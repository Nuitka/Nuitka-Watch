Xvfb :100 -nolisten tcp 2> >(grep -vE "_XSERVTrans|XKEYBOARD|xkbcomp|resolve keysym" >&2) &
DISPLAY=:100
export DISPLAY
