---
in_progress: yes
css_files: ../web/base.css ../web/manual.css ../web/help.css ../web/toc.css
body_css_class: width40 help-body
---

Oil Help
========

This doc describes every aspect of Oil briefly.  It underlies the `help`
builtin, and is indexed by keywords.

Navigate it with the [index of Oil help topics](oil-help-topics.html).

<!--
IMPORTANT: This doc is processed in TWO WAYS.  Be careful when editing.

It generates both HTML and text for the 'help' builtin.
-->

<div id="toc">
</div>

<h2 id="overview">Overview</h2>

### Usage

This section describes how to use the Oil binary.

<h4 id="oil-usage"><code>bin/oil</code> Usage</h4>

    Usage: oil  [OPTION]... SCRIPT [ARG]...
           oil [OPTION]... -c COMMAND [ARG]...

`bin/oil` is the same as `bin/osh` with a the `oil:all` option group set.  So
`bin/oil` also accepts shell flags.

    oil -c 'echo hi'
    oil myscript.oil
    echo 'echo hi' | oil

<h4 id="bundle-usage">App Bundle Usage</h4>

    Usage: oil.ovm MAIN_NAME [ARG]...
           MAIN_NAME [ARG]...

oil.ovm behaves like busybox.  If it's invoked through a symlink, e.g. 'osh',
then it behaves like that binary.  Otherwise the binary name can be passed as
the first argument, e.g.:

    oil.ovm osh -c 'echo hi'

<h3>Oil Lexing</h3>

<h4 id="single-command">single-command</h4>

The %%% prefix Starts a Single Command Over Multiple Lines (?)

This special lexer mode has several use cases:

Long command lines without trailing \

    %%% chromium-browser
        --no-proxy-server
        # comments allowed
        --incognito

Long pipelines or and-or chains without trailing \ 

    %%% find .
        # exclude tests
      | grep -v '_test.py'
      | xargs wc -l
      | sort -n

    %%% ls /
     && ls /bin
     && ls /lib
     || error "oops"

<h4 id="docstring">docstring</h4>

TODO

<h2 id="command">Command Language</h2>

#### proc

Procs are shell-like functions, but with named parameters, and without dynamic
scope (TODO):

    proc copy(src, dest) {
      cp --verbose --verbose $src $dest
    }

Compare with [sh-func]($osh-help).

#### equal

The `=` keyword shows the expression to its right:

    oil$ = 1 + 2*3
    (Int)   7

#### oil-block

Blocks can be passed to builtins (and procs eventually):

    cd /tmp {
      echo $PWD  # prints /tmp
    }
    echo $PWD

Compare with [sh-block]($osh-help).

<h2 id="assign">Assigning Variables</h2>

#### const 

Initializes a constant name to the Oil expression on the right.

    const c = 'mystr'        # equivalent to readonly c=mystr
    const pat = / digit+ /   # an eggex, with no shell equivalent

It's either a global constant or scoped to the current function.

#### var

Initializes a name to the Oil expression on the right.

    var s = 'mystr'        # equivalent to declare s=mystr
    var pat = / digit+ /   # an eggex, with no shell equivalent

It's either a global or scoped to the current function.

#### setvar

Like shell's `x=1`, `setvar x = 1` either:

- Mutates an existing variable (e.g. declared with `var`)
- Creates a new **global** variable.

It's meant for interactive use and to easily convert existing shell scripts.

New Oil programs should use `set`, `setglobal`, or `setref` instead of
`setvar`.

#### setglobal

Mutates a global variable.  If it doesn't exist, the shell exits with a fatal
error.

#### setref

Mutates a variable through a named reference.  TODO: Show example.

#### setlocal

Mutates an existing variable in the current scope.  If it doesn't exist, the
shell exits with a fatal error.

`set` is an alias for `setlocal` in the Oil language.  Requires `shopt -s
parse_set`, because otherwise it would conflict with the `set` builtin.  Use
`builtin set -- 1 2 3` to get the builtin, or `shopt -o` to change options.


<h2 id="word">Word Language</h2>

#### inline-call

#### splice

#### expr-sub

<h2 id="expr">Oil Expression Language</h2>

### Literals

#### oil-string

Oil strings appear in expression contexts, and look like shell strings:

    var s = 'foo'
    var double = "hello $world and $(hostname)"

However, strings with backslashes are forced to specify whether they're **raw**
strings or C-style strings:

    var s = 'line\n'    # parse error: ambiguous

    var s = c'line\n'   # C-style string
    var s = $'line\n'   # also accepted for compatibility

    var s = r'[a-z]\n'  # raw strings are useful for regexes (not eggexes)

#### oil-array

Like shell arays, Oil arrays accept anything that can appear in a command:

    ls $mystr @ARGV *.py

    # Put it in an array
    var a = %(ls $mystr @ARGV *.py)

#### oil-dict

#### oil-numbers

    myint = 42
    myfloat = 3.14
    float2 = 1e100

#### oil-bool

Capital letters to avoid confusions with the builtin **commands** `true` and
`false`:

    True T   False F

And the value that's unequal to any other:

    null

It's preferable to use the empty string in many cases.  The `null` value can't
be interpolated into words.

### Operators

#### concat

    mystr ++ otherstr
    "$mystr$otherstr"  # equivalent

    = mylist ++ otherlist

    setvar mydict = %{a: 1, b: 2}
    setvar otherdict = %{a: 10, c: 20}
    = mydict ++ otherdict

    setvar mystr ++= suffiX       # ???
    setvar mylist ++= %[item]
    setvar mydict ++= otherdict   # ???


#### oil-compare

    ==  <=  in

#### oil-logical

    not  and  or

#### oil-arith

    +  -  *  /   div  mod

`div` is for integer math, while `/` is for floating point math.

#### oil-bitwise

    ~  &  |  xor

#### oil-ternary

Like Python:

    display = 'yes' if len(s) else 'empty'

#### oil-index

Like Python:

    myarray[3]
    mystr[3]

TODO: Does string indexing give you an integer back?

#### oil-slice

Like Python:

    myarray[1 : -1]
    mystr[1 : -1]

#### func-call

Like Python:

    f(x, y)


### Eggex

#### re-literal

#### re-compound

#### re-primitive

#### named-class

#### class-literal

#### re-flags

#### re-multiline

Not implemented.

#### re-glob-ops

Not implemented.

    ~~  !~~


<h2 id="builtin">Builtin Commands</h2>

### Oil Builtins

### Data Formats

### External Lang

### Testing

<h2 id="option">Shell Options</h2>

<h3 id="strict:all">strict:all</h3>

#### strict_tilde

Failed tilde expansions cause hard errors (like zsh) rather than silently
evaluating to `~` or `~bad`.

#### strict_word_eval

TODO

#### strict_nameref

When `strict_nameref` is set, undefined references produce fatal errors:

    declare -n ref
    echo $ref  # fatal error, not empty string
    ref=x      # fatal error instead of decaying to non-reference

References that don't contain variables also produce hard errors:

    declare -n ref='not a var'
    echo $ref  # fatal
    ref=x      # fatal

#### parse_ignored

For compatibility, Oil will parse some constructs it doesn't execute, like:

    return 0 2>&1  # redirect on control flow

When this option is disabled, that statement is a syntax error.

<h3 id="oil:basic">oil:basic</h3>

#### simple_word_eval

TODO:

<!-- See doc/simple-word-eval.html -->

<h3 id="oil:all">oil:all</h3>

<h2 id="special">Special Variables</h2>

#### ARGV

Replacement for `"$@"`

#### STATUS

TODO: Do we need this in expression mode?

    if ($? == 0) {
    }
    if (STATUS == 0) {
    }

#### M

TODO: The match

### Platform

#### OIL_VERSION

The version of Oil that is being run, e.g. `0.9.0`.

TODO: comparison algorithm.

<h2 id="lib">Oil Libraries</h2>

### Collections

#### len()

- `len(mystr)` is its length in bytes
- `len(myarray)` is the number of elements
- `len(assocarray)` is the number of pairs

`copy()`:

```
var d = {name: value}

var alias = d  # illegal, because it can create ownership problems
               # reference cycles
var new = copy(d)  # valid
```

### Pattern

- `regmatch(/d+/, s)` returns a match object
- `fnmatch('*.py', s)`  returns a boolean

### String

### Better Syntax

These functions give better syntax to existing shell constructs.

- `shquote()` for `printf %q` and `${x@Q}`
- `lstrip()` for `${x#prefix}` and  `${x##prefix}`
- `rstrip()` for `${x%suffix}` and  `${x%%suffix}` 
- `lstripglob()` and `rstripglob()` for slow, legacy glob
- `upper()` for `${x^^}`
- `lower()` for `${x,,}`
- `strftime()`: hidden in `printf`

### Arrays

- `index(A, item)` is like the awk function

### Assoc Arrays

- `@names()`
- `values()`.  Problem: these aren't all strings?

### Block

<h3>libc</h3>

<h4 id="strftime">strftime()</h4>

Useful for logging callbacks.  NOTE: bash has this with the obscure printf
'%(...)' syntax.

### Hashing

TODO

