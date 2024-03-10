# Tmux Workshop


# Introduction

* Fascination with tooling, big enough to be useful, small enough to be doable, i.e. no Vim. See my previous talks.
* The sea of craziness metaphor: safe and bland vs. very customized but unsupported
* "What if I told you that one terminal window is all you need?"
 - no need for separate tabs or terminal windows or a separate terminal in VS Code and iTerm, it's all the same terminal, same environment, with the same history.

## Why Tmux?
* meme about site hosting
* build development environment
* make administration/deploy/monitoring dashboard
* `exit` or `^D`
* For a long time Resisted learning systemd, one of my production services was a tmux-session.

# Basic Usage
 `*` (current) and `-` (previous) semantics, same as bash or git.
* `base-index` set to 1 for ease of keyboard access, `pane-base-index` for panes
* `renumber-windows` to avoid having holes in window numbers
* for complete focus zoom with Z, hide status bar with `set -g status`
* for 256 colors `tmux -2 a`
* show the time `t`

---
* basic start
* start a long-running command
* dettach with `prefix-d`
* re-attach with `tmux attach` or `tmux a`
---


## Preset layouts
* `prefix-space`
* `display-panes`
* display-panes timeout + reload
* default: select-pane, change to kill pane, see `template` arg
* `main-pane-height`, `main-pane-width width`, `other-pane-height`, `other-pane-width`
* prefix-f to find the window: full-text search in what is shown in the pane.

# Theory

* server, client, session, window, pane, status line, commands
* a session can have any number of windows
* clients can connect to the same tmux session: one server, many clients
* session is a collection of pseudo terminals, organized in windows and panes
* tmux exits when the last session is killed
* pty(4) for technical info on pseudo terminals, `echo $TMUX`
* client and server are separate processes, communicate via socket in `/tmp`

## Config

* `-f some_tmux.conf` > `~/.tmux.conf` > `/etc/tmux.conf`
* use `source-file` command to load a config
* config loaded once, errors are displayed but ignored, e.g. version change


# Usability
* clients seem superfluous, but useful when you connect to the same session from VS code and iTerm.
 - `choose-tree` or prefix-w

* Windows linked between sessions: cmus?
* `set synchronize-panes` for doing the same operation on multiple servers
* prefix: same everywhere, thus digging else `^b` for local `^a` for remote.

## Screenshoting a pane
* `capture-pane` TODO, doesn't seem to work

## Recording a Session
* `pipe-pane`

# Options
* on/off options can be toggled without specifiying `on`/`off`
* user options seem interesting, prefixed with `@`
* `cusomize-mode` to see all options

# Key Binding
* `list-keys` to see the default bindings
* `C-b ?` shows help
* C-b /       Describe key binding
* bind key to the root table, no need for prefix now you can finally put those silly function keys to use!
 - default root is quite bland, only mouse events with up to triple (!) mouse
* create your own table on top of existing four.

---

# UI

## Status Line
* status line can be up to 5 lines tall
* status-interval default is 15 seconds, change to 1 second for faster refresh, e.g. show seconds in time
* Space left on disk, for those dockering around

* display-{message,popup,menu}j
## Popups

### Building a widget

* `display-popup -E -T Calendar -w 23 -h 11 "cal -N && read -n 1 -s -r"`
** check for bound keys with prefix-/
** bind-key -N "Display a fortune" F display-popup -E -T Fortune -w 80 -h 10 "fortune && read -n 1 -s -r"
** bind it to a key
** add note `show calendar`
** prefix-/ to see the note
** prefix-? to see the list
** save key to tmux-config TODO how to paste from history?

## Menus

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

It demonstrate almost too many features of Tmux.

### Klarna shortcuts

* starting name with `-` makes an item disabled
* add a `''` for a separator

## Borders
* pane-border-indicators [off | colour | arrows | both] is quite neat
* `popup-border-lines` rounded is cool

## Formats

* Conditionals: show mousy icon in my right status.
** regular expressions are supported when simple string comparison is not enough 
* Numeric operators: default integer/float optional
* `#{e|*|f|4:5.5,3}`  for a complicated calculator
* `#{a:64}` for ASCII lookup
* `#{c:turquoise}` for color to RGB hex code
* padding, truncating, substitution
* strftime
* run shell command, e.g. `#(whoami)`

## Styles #[...]

* fg=, bg=
** black, red, green, yellow, blue, magenta, cyan, white;
** brightred, brightgreen, brightyellow
** colour0 to colour255
** hex-code e.g. #ffffff
* align: left, center, right
* best way to play is in status line 


### Format Variables
* there are abbreviations for commonly used ones e.g. `#H` for `host`, `#S` for `session_name`.
* `display-message "#{cursor_character}"
---

# Copy Mode
* scrollback and search in history for error message

# Mouse Usage
* mouse right-click to select menu items
 - swap marked from mouse menu
** (Pane, Border, Status, Status, StatusLeft, StatusRight, StatusDefault) x (WheelUp/WheelDown, Down/Up/Drag, Double/Triple click) create your own crazy interface.
** {mouse} as the target for commands.
* Draw a table of possible events and their targets

# Bad (?) ideas
* cat own socket to break tmux
* Pomodoro in Tmux?
* Pipe pane can be used also for input: `:pipe-pane -I "echo 'echo hello'"`
 - Funnily enough, both input and output can be enabled for pipe-pane. So, if you want to give some script both input and output access to your terminal, tmux can help you with that.

==========================

HERE BE DRAGONS

==========================

---
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


# Random Stuff

* maxing out scrollback buffer
* "You have control" -> "I have control" shared screen routine
* `split-window vim foo.txt` opens a split and runs the command
* tmux commands for starting pre-set window layouts and commands
* (mouse events) x (areas) diagram
* `tmux lsp -F '#{session_id} #{window_id} #{pane_id}'`
* `[ -n "$TMUX" ] && echo inside tmux`

```
%if #{==:#{host_short},firsthost}
  source ~/.tmux.conf.firsthost
%elif #{==:#{host_short},secondhost}
  source ~/.tmux.conf.secondhost
%endif
```

* own key table

# Links

* https://tmuxcheatsheet.com/
* https://habr.com/en/post/165437/
* https://pragprog.com/book/bhtmux2/tmux-2
* https://github.com/christoomey/vim-tmux-navigator
* https://iterm2.com/documentation-tmux-integration.html
* https://raw.githubusercontent.com/tmux/tmux/3.2a/CHANGES - aka what's new
