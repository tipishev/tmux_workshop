# tmux Workshop

# Transcript

Welcome to today's workshop. My name is Tim, I am a Competence Lead for Batch Variables team. If you have been to my previous talks on Git, Python debuggers, and TiddlyWiki, you know that I am fascinated with tooling. I like to present tools that are not too big, but nevertheless useful. Today I will show how tmux can boost your productivity when working with terminal applications. I have been using tmux on and of for about 10 years now, and I prepared this workshop to fill the gaps I had. This session consists of 4 parts. In the first I show what tmux and its basic usage. In the second part I explain the architecture of it, namely what are the sessions, clients, windows, and panes. In the third part I will show how tmux operate on these entities with its rich set of commands. In the final part I will show how to add bells and whistles that makes tmux experience smooth for you as a user.

Whenever we discuss tooling, I use the sea of craziness metaphor: safe and bland vs. very customized but unsupported.

> cli_stack.png

## Part 1: Down the Memory Lane

Tmux is a short for terminal multiplexer. It's a command line tool that holds the state of one or more terminals. To put it simply, imagine running a command in a terminal, as soon as you close the terminal, the program receives a `SIGHUP` signal that makes it exit.

> open terminal.app, start python, close the terminal.

This is fine for running locally, but becomes a problem when you SSH to a remote host, start a long-running command and your connection drops. To deal with this we need to spawn a proxy-process that persists the command's run state. I first encountered this problem back at university when I missed on all the fun conversation on Computer Science IRC channel when I was offline since IRC did not keep message history. At the time this was solved with a tool called GNU screen: I would SSH to the university server, start screen,and run IRC client inside it. When I reconnected to the server, screen was happily holding my chat client unless the server underwent a maintenance reboot. In one of these chat sessions my clubmate was excited about this new tool, tmux, which he described as screen on steroids, so we got it installed on our club's server.

This was THE use case for many people, as you can see from tmux's picture on Wikipedia:

> show [tmux Wikipedia page](https://en.wikipedia.org/wiki/tmux)

Later, I would shamefully use tmux to run web servers instead of learning systemd. Now, that I look at all of today's complexity of hosting a website, I realize that it was notsuch a bad idea.

> show the `gymnast_girl.jpg`

It is at that time I started learning about other features of tmux, my favorite was showing multiple split-terminals at once. I would start the server in one split, open the logs in the second, and run `htop` to show the server CPU and memory usage.

> show `server_dashboard.png`

Now I realize that tmux gave me a service dashboard that took just a minute to setup.

A little later, when I learned Vim and became obsessed with running everything in terminal, I started using tmux locally as my IDE and wanted to learn everything there is about it. This image from an online book [Tao of Tmux](https://tao-of-tmux.readthedocs.io/en/latest/index.html) (read it!) finally made it click for me:

> show `tao_of_tmux.png`

When we run `tmux`, it creates a server. The server is a container for sessions, sessions contain windows, and windows contain panes. Let me demonstrate this.

>>>
* run `tmux`
* `C-b $` give name "Klarna"
* `C-b ,` give name "first window"
* `C-b %`  # a vertical split
* `C-b "`  # a horizontal split
* `C-b right left` # to move horizontally
* `C-b down up` # to move vertically
* `C-b c`, `C-,` give name "second window"
* `C-b &` to close a window, or just close the last pane with `Ctrl-D`
* `C-b 1` `C-b 2` to go between numbered windows
* `C-b d` # dettach
* run `tmux`
* `C-b $` give name "Personal"
* `C-b w` # display the whole tree with 2 sessions, 3 windows, and their splits
>>>

At this point you may realize, that one terminal is all you need. No need to bother your GUI with windows, tabs, and splits, tmux got you covered. 

> morpheus.png

At this point, may I suggest to you Alacritty, a blazingly fast GPU-accelerated terminal written in Rust that does exactly this: one window, dead simple text config and zero tabs.

Now you may be saying, but what about my IDE? It also has a terminal. No worries, tmux got you covered: just connet to the same session and this will create another client, connected to the same tmux session:

> `:list-clients`

The session is closed, once the last window in it is closed.

Whatever you do in one client is synchronized to every other. That's how my friend and I used to pair-play text-based adventures, we would both SSH to my server, start a Frotz client and take turns typing in commands, passing turns copilot-style: "You have control" -> "I have control".

> copilots.png

# Introduction


# Basic Usage
* `base-index` set to 1 for ease of keyboard access, `pane-base-index` for panes
* `renumber-windows` to avoid having holes in window numbers
* remark on attention span and importance of tabs ordering in browser and windows
* for complete focus zoom with Z, hide status bar with `set -g status`
* for 256 colors `tmux -2 a`
* show the time `t`

## Preset layouts
* `prefix-space`
* `display-panes`
* display-panes timeout + reload
* default: select-pane, change to kill pane, see `template` arg
* `main-pane-height`, `main-pane-width width`, `other-pane-height`, `other-pane-width`
* prefix-f to find the window: full-text search in what is shown in the pane.

## Config

* `-f some_tmux.conf` > `~/.tmux.conf` > `/etc/tmux.conf`
* use `source-file` command to load a config
* config loaded once, errors are displayed but ignored, e.g. version change


# Usability
* `set synchronize-panes` for doing the same operation on multiple servers
* prefix: same everywhere, thus digging else `^b` for local `^a` for remote.

## Screenshoting a pane
* `capture-pane` TODO, doesn't seem to work

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

It demonstrate almost too many features of tmux.

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
* Pomodoro in tmux?
* Pipe pane can be used also for input: `:pipe-pane -I "echo 'echo hello'"`
 - Funnily enough, both input and output can be enabled for pipe-pane. So, if you want to give some script both input and output access to your terminal, tmux can help you with that.

==========================

HERE BE DRAGONS

==========================

Status icon for background apps?

---
* `tmux list-sessions` -> `tmux ls`
* `Pr-w` for an interactive overview
* `Pr-f` for string search
* `Pr-&` end it all, with confirmation
* `Pr-%`, `Pr-"`, `Pr-o`, `Pr-arrows` for moving between splits
* `^<space>` for pre-set layouts

* `Pr-?` for current key-bindings, TODO run it


### Windows

* move with `.`, pro-tip: autonumber to allow moving to `0` and `99`  focus and tab-stack
* `f` search window for text
* `i` window info, too fast? use `~` to see tmux messages
* go to bell/activity `M-n` / `M-o`

### Panes

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
* `bind-key R source-file ~/.tmux.conf; display-message "config reloaded"`

* Group panes `join-pane -t :{window number}`


# Random Stuff

* maxing out scrollback buffer
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
