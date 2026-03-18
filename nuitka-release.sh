#!/bin/bash

ARGS=()
TEST_HOTFIX=0

for arg in "$@"; do
    if [ "$arg" = "--test-hotfix" ]; then
        TEST_HOTFIX=1
    else
        ARGS+=("$arg")
    fi
done

if [ "$TEST_HOTFIX" = "1" ]; then
    cd ../Nuitka-develop || exit 1

    if git config remote.github.url > /dev/null; then
        REMOTE="github"
    else
        REMOTE="origin"
    fi

    echo "Checking for hotfix branches on $REMOTE remote..."

    HOTFIX_BRANCHES=$(git ls-remote "$REMOTE" "refs/heads/hotfix/*" | awk '{print $2}' | sed 's|^refs/heads/||')

    if [ -z "$HOTFIX_BRANCHES" ]; then
        echo "Error: No hotfix branches found on $REMOTE remote."
        exit 1
    fi

    COUNT=$(echo "$HOTFIX_BRANCHES" | wc -l)

    if [ "$COUNT" -gt 1 ]; then
        echo "Error: Multiple hotfix branches found on $REMOTE remote:"
        echo "$HOTFIX_BRANCHES"
        exit 1
    fi

    echo "Found hotfix branch: $HOTFIX_BRANCHES"
    git fetch -p "$REMOTE" || exit 1
    git checkout -B "$HOTFIX_BRANCHES" "$REMOTE/$HOTFIX_BRANCHES" || exit 1

    cd - > /dev/null || exit 1
fi

exec ./run-watch.sh --no-pipenv-update "${ARGS[@]}"
