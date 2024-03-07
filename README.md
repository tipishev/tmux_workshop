# Tmux Workshop

Here I aggregate my notes and slides for a workshop on Tmux.

---

TODO add SSH access to the container

```bash
docker build -t tmux-tutorial .
docker run -it tmux-tutorial
```

`tmux new -s ""`

prefix-Q -> choose the pane

`tmux new -n "my top window" top`

 `*` (current) and `-` (previous) semantics, same as bash or git.

> C-M-x means pressing the control key, meta key and x together.

* `C-b ?` shows help
* C-b /       Describe key binding
* copy-mode
---

Let's take the most complex command from `list-keys`

`prefix->`


```
display-menu -T "#[align=centre]#{pane_index} (#{pane_id})" -x P -y P "#{?#{m/r:(copy|view)-mode,#{pane_mode}},Go To Top,
}" < { send-keys -X history-top } "#{?#{m/r:(copy|view)-mode,#{pane_mode}},Go To Bottom,}" > { send-keys -X history-bottom } '' "#{?mouse_word,Search For #[underscore]#{=
/9/...:mouse_word},}" C-r { if-shell -F "#{?#{m/r:(copy|view)-mode,#{pane_mode}},0,1}" "copy-mode -t=" ; send-keys -X -t = search-backward "#{q:mouse_word}" } "#{?mouse_w
ord,Type #[underscore]#{=/9/...:mouse_word},}" C-y { copy-mode -q ; send-keys -l "#{q:mouse_word}" } "#{?mouse_word,Copy #[underscore]#{=/9/...:mouse_word},}" c { copy-mo
de -q ; set-buffer "#{q:mouse_word}" } "#{?mouse_line,Copy Line,}" l { copy-mode -q ; set-buffer "#{q:mouse_line}" } '' "Horizontal Split" h { split-window -h } "Vertical
 Split" v { split-window -v } '' "#{?#{>:#{window_panes},1},,-}Swap Up" u { swap-pane -U } "#{?#{>:#{window_panes},1},,-}Swap Down" d { swap-pane -D } "#{?pane_marked_set
,,-}Swap Marked" s { swap-pane } '' Kill X { kill-pane } Respawn R { respawn-pane -k } "#{?pane_marked,Unmark,Mark}" m { select-pane -m } "#{?#{>:#{window_panes},1},,-}#{
?window_zoomed_flag,Unzoom,Zoom}" z { resize-pane -Z }
```

It demonstrate almost many features of Tmux.



---

# Tricks

## Building a widget

* fortune with Sun Tzu quotes?

* `display-popup -E -T Calendar -w 23 -h 11 "cal -N && read -n 1 -s -r"`
** check for bound keys with prefix-/
** bind-key -N "Display a fortune" F display-popup -E -T Fortune -w 80 -h 10 "fortune && read -n 1 -s -r"
** bind it to a key
** `cusomize-mode`
** add note `show calendar`
** prefix-/ to see the note
** prefix-? to see the list
** save key to tmux-config TODO how to paste from history?

## Multi-terminal SSH

* `set synchronize-panes` for doing the same operation on multiple servers

## Preset layouts

* prefix-space
* display-panes
* display-panes timeout + reload
* default: select-pane, change to kill pane, see `template` arg

* `capture-pane` is a screenshot

* `choose-tree` or prefix-w

* prefix-f to find the window: full-text search in what is shown in the pane.

## Key Bindings

* `list-keys` to see the default bindings

---

# Pre-requisites

* familiarity with command line
* Docker installed on local system
* instructions on how to install for the big 3 OSes

# Misceallaneous

* Fascination with tooling, big enough to be useful, small enough to be doable, i.e. no Vim. See my previous talks.
* The sea of craziness metaphor: safe and bland vs. very customized but unsupported
* For a long time Resisted learning systemd, one of my production services was a tmux-session.
* "What if I told you that one terminal window is all you need?"
** no need for separate tabs or terminal windows or a separate terminal in VS Code and iTerm.

# Theory

## The book

* build development environment
* make administration/deploy/monitoring dashboard
* tmate? as alternative to pair programming
* plugins?
* `tmux new-session -s basic` shorten to `tmux new -s basic`
* `exit` or `^D`
* prefix: same everywhere, thus digging else `^b` for local `^a` for remote.
* `tmux list-sessions` -> `tmux ls`
* `tmux new -s second_session -d` to start a session in the background.
* `tmux kill-session -t basic`
* `tmux new -s windows -n shell`
* `Pr-n`/`Pr-p` for cycling between windows
* `Pr-w` for an interactive overview
* `Pr-f` for string search
* `Pr-&` end it all, with confirmation
* `Pr-%`, `Pr-"`, `Pr-o`, `Pr-arrows` for moving between splits
* `^<space>` for pre-set layouts
* `:new-window -n processes "htop"`

* `Pr-?` for current key-bindings, TODO run it


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
* start a long-running command
* dettach with `prefix-d`
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
* ~e~and it all.. with `&`
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
* writing log to file for postmortem, Prefix-P in my config
* lure away from using `screen`
* "You have control" -> "I have control" shared screen routine
* `split-window vim foo.txt` opens a split and runs the command
* tmux commands for starting pre-set window layouts and commands

# Links

* https://tmuxcheatsheet.com/
* https://habr.com/en/post/165437/
* https://pragprog.com/book/bhtmux2/tmux-2
* https://github.com/christoomey/vim-tmux-navigator
* https://iterm2.com/documentation-tmux-integration.html
* https://raw.githubusercontent.com/tmux/tmux/3.2a/CHANGES - aka what's new
