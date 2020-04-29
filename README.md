# Tmux Workshop

Here I aggregate my notes and slides for a workshop on Tmux.

# Theory

## `man tmux`

* session, window, pane, status line, commands
* pty(4) for technical info on pseudo terminals
* session is a collection of pseudo terminals, organized in windows and panes
* clients can connect to the same tmux session: one server, many clients
* a session can have any number of windows
* tmux exits when the last session is killed



# practice

## Basic Usage

* show basic start/run long command/dettach/re-attach
* for 256 colors `tmux 2 a` to remind about wishing for a 2:a near Tunnelbana
* create more than one session, show list (`tmux ls`), give names, selective attach

## Tweaking Status Line

* Space left on disk, for those dockering around


# Links
https://habr.com/en/post/165437/
https://pragprog.com/book/bhtmux2/tmux-2
