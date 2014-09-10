#!/bin/bash
# ----------------------------------------------------------------------------------------------------------------------
# OBITEC Django Installer
# ----------------------------------------------------------------------------------------------------------------------
# Setup and create a new Django project based on OBITECS' djskel template.


# LICENSE
# ----------------------------------------------------------------------------------------------------------------------
# Copyright (c) 2014 OBITEC Consultig (Pty) Ltd
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# SETTINGS
# ----------------------------------------------------------------------------------------------------------------------
# Max number of arguments, empty value = unlimited arguments
SCRIPT_MAX_ARGS=1


# INITIALIZE
# ----------------------------------------------------------------------------------------------------------------------
SCRIPT_NAME="$(basename "$0")"
# Stores arguments
SCRIPT_ARGS=()
# Stores option flags
kwargs=()
# For returning value after calling get_kwarg
kwarg_value=

normal=$(tput sgr0)
bold=$(tput bold)
red=$(tput setaf 1)
green=$(tput setaf 2)
yellow=$(tput setaf 3)
blue=$(tput setaf 4)
magenta=$(tput setaf 5)
cyan=$(tput setaf 6)


# BOILERPLATE FUNCTIONS
# ----------------------------------------------------------------------------------------------------------------------
# Usage for -h|--help
usage () {
  echo "Usage: $SCRIPT_NAME [options] [arguments]

OPTIONS:
    --no-color   do not use colors
    -h, --help   display this help and exit

EXAMPLES:
    $SCRIPT_NAME demo_project --app=demo_app --python=/usr/bin/python
"
}

# Usage: info "message"
# Example: info "It's Working"
# Output (to STDOUT): [...] It's Working
info (){
    printf "%b" "[${green}...${normal}] $1\n"
}

# Usage: prompt "question"
# Example: prompt "What's Your Name?"
# Output (to STDOUT): [ ? ] What's Your Name?  
prompt (){
    printf "%b" "[${yellow} ? ${normal}] $1 "
}

# Usage: error ["message"]
# Example: error "You're Ugly"
# Output (to STDERR): [ERROR] /script/name: You're Ugly
error (){
    printf "%b" "[${red}ERROR${normal}] ${0}: ${1:-'Unkown Error'}\n" >&2
}

# Usage: fail "message" [exit_code]
# Example: fail "Unknown Option" 254
fail (){
    error "$1"

    case $2 in
        ''|*[!0-9]*)
            exit_code=1
            ;;
        *)
            exit_code=$2
        ;;
    esac

    #echo "$SCRIPT_NAME: invalid option -- '$opt'" >&2
    #echo "Try \`$SCRIPT_NAME --help' for more information." >&2

    exit ${exit_code}
}

# ask function https://gist.github.com/davejamesmiller/1965569
# Usage: ask "Yes or No?" [default option]
# Example: if "Yes or No?" Y; then
ask (){
    while true; do
 
        if [ "${2:-}" = "Y" ]; then
            prompt_tail="Y/n"
            default=Y
        elif [ "${2:-}" = "N" ]; then
            prompt_tail="y/N"
            default=N
        else
            prompt_tail="y/n"
            default=
        fi
 
        # Ask the question
        prompt "$1 [$prompt_tail]"
        read REPLY
 
        # Default?
        if [ -z "$REPLY" ]; then
            REPLY=$default
        fi
 
        # Check if the reply is valid
        case "$REPLY" in
            Y*|y*) return 0 ;;
            N*|n*) return 1 ;;
        esac

    done
}

# Usage: show_help [exit_code]
# Example: show_help 254
show_help (){
    cat <<HELP
    Usage:
        $0 [OPTION]...

    OPTIONS:
        --help, -h:    Show this help and exit

    Example:
        $0 **example**

HELP

    # Fail with general error if status code passed
    case $1 in
        ''|*[!0-9]*)
            exit_code=1
            ;;
        *)
            exit_code=$1
        ;;
    esac

    exit ${exit_code}
}

argument_expected(){
    fail "$1 expected an argument"
}

finally(){
    if [ ! -z $example_one ]; then
        info "Finally, Example One: \"$example_one\""
    fi

    if [ ! -z $example_two ]; then
        info "Finally, Example Two: \"$example_two\""
    fi

}

parse_options() {
  while (( $#>0 )); do
    opt="$1"
    arg="$2"
    
    case "$opt" in
      -p|--python-path)
        kwarg_set "python_path" "$arg" 1
        shift
        ;;
      -a|--app-name)
        kwarg_set "app_name" "$arg" 1
        ;;
      --no-color)
        kwarg_set "no-color"
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      -*)
        echo "$SCRIPT_NAME: invalid option -- '$opt'" >&2
        echo "Try \`$SCRIPT_NAME --help' for more information." >&2
        exit 1
        ;;
      *)
        if [[ ! -z ${SCRIPT_MAX_ARGS} ]] && (( ${#SCRIPT_ARGS[@]} == ${SCRIPT_MAX_ARGS} )); then
          echo "$SCRIPT_NAME: cannot accept any more arguments -- '$opt'" >&2
          echo "Try \`$SCRIPT_NAME --help' for more information." >&2
          exit 1
        else
          SCRIPT_ARGS=("${SCRIPT_ARGS[@]}" "$opt")
        fi
        ;;
    esac
    shift
  done
}

check_args(){
    while [ ! -z "$1" ]; do
        local arg="$1"
        case "$1" in
            -h|--help) 
                local help=0
                shift
                ;; 
            -ex1|--example-one)
                shift

                if [ -z $1 ] || [[ "$1" == -* ]]; then
                    argument_expected $arg
                fi

                example_one=$1
                shift
                ;;
            -ex2|--example-two)
                # Simple boolean flag–call function here
                example_two="Two"
                shift
                ;;
            -*)
                fail "Unknown option $1"
                shift
                ;;
            *)
                echo "Project name: $1"
                shift
                ;;
        esac
    done

    if [ ! -z ${help} ]; then
        show_help ${help}
    fi

    finally

    exit 0
}

# SCRIPT TEMPLATE FUNCTIONS
# ----------------------------------------------------------------------------------------------------------------------
# Stores options
# $1 - option name
# $2 - option value
# $3 - non-empty if value is not optional
kwarg_set () {
  if [[ ! -z "$3" ]] && [[ -z "$2" ]]; then
    echo "$SCRIPT_NAME: missing option value -- '$opt'" >&2
    echo "Try \`$SCRIPT_NAME --help' for more information." >&2
    exit 1
  fi
  # XXX should check duplication, but doesn't really matter
  kwargs=("${kwargs[@]}" "$1" "$2")
}

# Checks if an option is set, also set kwarg_value.
# Returns 0 if found, 1 otherwise.
get_kwarg () {
  local i opt needle="$1"
  for (( i=0; i<${#kwargs[@]}; i+=2 )); do
    opt="${kwargs[i]}"
    if [[ "$opt" == "$needle" ]]; then
      kwarg_value="${kwargs[i+1]}"
      return 0
    fi
  done
  kwarg_value=
  return 1
}

set_color_variables () {
  local COLORS=(BLK RED GRN YLW BLU MAG CYN WHT)
  local i SGRS=(RST BLD ___ ITA ___ BLK ___ INV)
  for (( i=0; i<8; i++ )); do
    eval "F${COLORS[i]}=\"\e[3${i}m\""
    eval "B${COLORS[i]}=\"\e[4${i}m\""
    eval   "T${SGRS[i]}=\"\e[${i}m\""
  done
}



# FUNCTIONS
# ----------------------------------------------------------------------------------------------------------------------
check_python(){
    if type python3 2>&-; then
        echo "Found Python 3:" >&2
    else
        echo "Python3 not found, attempting install..." >&2
    fi
}

create_project(){
    project_name = ${SCRIPT_ARGS[0]}
    echo "Creating project '${project_name}'..." >&2
    command mkproject ${project_name} --system-site-packages

}

# MAIN
# ----------------------------------------------------------------------------------------------------------------------
main(){
    if [ -z $1 ]; then
        usage
    fi

    if ! get_kwarg "no-color"; then
      set_color_variables
    fi

    #check_args "$@"
    parse_options "$@"

    check_python
    create_project



    
}

main "$@"
