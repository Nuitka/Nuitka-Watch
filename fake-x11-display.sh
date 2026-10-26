# Sets up a fake X display for the GUI test cases, sourced from run-watch.sh.
#
# A server that is already running for the display is reused.  Starting a
# second one would fail with "Server is already active for display 100",
# and a lock file left behind by an earlier crash can make it fail with
# "Could not write pid to lock file in /tmp/.tX100-lock".

X11_DISPLAY="${NUITKA_WATCH_X11_DISPLAY:-:100}"
X11_DISPLAY_NUMBER="${X11_DISPLAY#:}"
X11_DISPLAY_NUMBER="${X11_DISPLAY_NUMBER%%.*}"

x11_display_up()
{
    local display="$1"

    if [ -z "$display" ]
    then
        return 1
    fi

    if command -v xdpyinfo > /dev/null 2>&1
    then
        xdpyinfo -display "$display" > /dev/null 2>&1
    else
        local number="${display#:}"
        number="${number%%.*}"

        local pid=`cat "/tmp/.X${number}-lock" 2> /dev/null`

        [ -n "$pid" ] && kill -0 "$pid" 2> /dev/null
    fi
}

x11_start_server()
{
    local log=`mktemp /tmp/nuitka-watch-xvfb.XXXXXX`
    local old_lock="/tmp/.tX${X11_DISPLAY_NUMBER}-lock"

    # The temporary lock file only exists while a server is starting up, so
    # a leftover from a crash can be removed safely, it would only make the
    # next start fail.
    if [ -n "`find "$old_lock" -maxdepth 0 -mmin +1 2> /dev/null`" ]
    then
        rm -f "$old_lock"
    fi

    Xvfb "$X11_DISPLAY" -nolisten tcp > /dev/null 2> "$log" &

    local i
    for i in {1..50}
    do
        if x11_display_up "$X11_DISPLAY"
        then
            # Harmless warnings, not worth keeping around.
            rm -f "$log"
            return 0
        fi

        sleep 0.2
    done

    echo "Failed to start fake X display on $X11_DISPLAY:" >&2
    grep -vE "_XSERVTrans|XKEYBOARD|xkbcomp|resolve keysym" "$log" >&2 || true
    rm -f "$log"

    return 1
}

if ! x11_display_up "$X11_DISPLAY"
then
    # Serialize concurrent watch runs, so that only one of them starts the
    # server and the others just reuse it.
    if command -v flock > /dev/null 2>&1
    then
        exec 9> "/tmp/.nuitka-watch-x11-${X11_DISPLAY_NUMBER}.lock"
        flock 9
    fi

    if ! x11_display_up "$X11_DISPLAY"
    then
        x11_start_server || true
    fi

    if command -v flock > /dev/null 2>&1
    then
        flock -u 9
        exec 9>&-
    fi
fi

if x11_display_up "$X11_DISPLAY"
then
    DISPLAY="$X11_DISPLAY"
    export DISPLAY
fi
