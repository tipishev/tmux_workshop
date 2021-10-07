# Tmux Workshop

Here I aggregate my notes and slides for a workshop on Tmux.

# Backstory

It's year 2022, following the virus outbreak economy is in decline, desktop and web applications are rapidly fading into obscurity due to continued [software disenchantment](https://tonsky.me/blog/disenchantment/), bandwidths have shrunk to dialup and command line apps are all the rage. The medical tyranny has forbidden all the mice since they spread infections. A new kind of developer is in high demand. Those who can combine textual information in terminals. You discover an almost forgotten art of tmuxing: creating persistent collections of pseudoterminals.

# Theory

## `man tmux`

* server, client, session, window, pane, status line, commands
* pty(4) for technical info on pseudo terminals
* session is a collection of pseudo terminals, organized in windows and panes
* clients can connect to the same tmux session: one server, many clients
* a session can have any number of windows
* tmux exits when the last session is killed
* client and server are separate processes, communicate via socket in `/tmp`
* CONTROL MODE? -CC disables echo
* can execute command via `-c` flag
* `command [flags]` can be sent as the last argument to tmux


### Config

* `-f some_tmux.conf` > `~/.tmux.conf` > `/etc/tmux.conf`
* use `source-file` command to load a config
* config loaded once, errors are displayed but ignored, e.g. version change

### Sockets

* `-L socket-name` to allow multiple tmux servers to run
* by default the socket is `default` and stored in `$TMUX_TMPDIR` or `/tmp`
* `-S socket-path` to provide a complete path to socket, ignores `-L` flag

### Miscellaneous flags

* `-u` to force unicode support
* `-vv` logs everything, but not very useful, try when no server has started

### Colors

* for 256 colors `tmux -2 a`

### CLIENTS AND SESSIONS


# Practice

## Basic Usage

* basic start
* run long command
* dettach with `d`
* re-attach with `tmux attach` or `tmux a`

### Bonus

* show the time `t`

## Intermediate Usage


### Sessions

* create more than one session
* show list (`tmux ls`)
* name session with `$`
* selective attach `tmux a -t {name prefix}`
* `)` and `(` for cycling between sessions
* `s` interactive attach
* `L` to quickly switch between most recent sessions
* `D` choose a client to dettach (useful?)

### Windows

* create window `c`
* switch between numbered windows
* name window with `,`
* ~e~ and it all.. with `&`
* move with `.`, pro-tip: autonumber to allow moving to `0` and `99`
* `f` search window for text
* `i` window info, too fast? use `~` to see tmux messages
* go to bell/activity `M-n` / `M-o`

### Panes

* create splits `%` for vertical, `"` for horizontal
* arrows to navigate, pro-tip: vi-keys
* resize with `C-arrows`, mega-resize with `M-arrows`
* kill with `x`
* change layout with `C-space`
* rotate splits with `C-o`
* switch with `{`/`}`
* quick-switch in the same window `;` or `l`
* zoom on pane: `z`
* breakout `!` when a pane gets promoted to a window
* `q` display indexes and sizes
* `m` mark, `M` unmark

### Bonus

* `w` interactive windows list, hotkeys

## Buffers

From the olden days of window point-and-click buffers were useful, so tmux improved on this and added multiple buffers.

* `[` enter copy mode, also with `PgUp`
* `]` paste
* `#` list paste buffers
* `=` choose what to paste
* `-` delete most recent paste buffer

## Commands

A whole new beast: `:`

Hello world: `display-message hello!`

Targeting with `-t` (target) and sometimes `-s` (source)

* `target-client`: /dev/ttyp1
* `target-session`: 4 rules
* `target-window`: 6 rules... and special symbols
* `target-pane`: special tokens, including relative positions and offsets

* if you have smuggled a mouse, use `{mouse}` to get target.
* `{marked}` can be also used

* sessions `$` , windows `@`, panes `%` have id, immutable, on server
* `$TMUX`, `$TMUX_PANE`

* `list-sessions`, `list-windows`, `list-panes`
* `session_id`, `window_id`, or `pane_id` FORMATS
* pass command to execute to
  - `new-window`
  - `new-session`
  - `split-window`
  - `respawn-window`
  - `respawn-pane`
* `bind-key F1 set-window-option force-width 81` from inside Tmux
* `tmux bind-key F1 set-window-option force-width 81` from outside Tmux
* `bind-key R source-file ~/.tmux.conf; display-message "config reloaded"`

* Group panes `join-pane -t :{window number}`


## Tweaking Status Line

* Space left on disk, for those dockering around

# Random Stuff

* maxing out scrollback buffer
* writing log to file for postmortem
* lure away from using `screen`
* "You have control" -> "I have control" shared screen routine
* `split-window vim foo.txt` opens a split and runs the command
* tmux commands for starting pre-set window layouts and commands


# Links

* https://habr.com/en/post/165437/
* https://pragprog.com/book/bhtmux2/tmux-2
* https://github.com/christoomey/vim-tmux-navigator
* https://iterm2.com/documentation-tmux-integration.html
* https://raw.githubusercontent.com/tmux/tmux/3.2a/CHANGES - aka what's new
