# get request format for actuation

http://gabriele2003.comelitdns.com:90/user/action.cgi?type=light&num0=0

- type: light, shutter, other (depends on category)
- numx: x is 1 for on and 0 for off
- =y: y is the unique device id

# updating

http://gabriele2003.comelitdns.com:90/user/icon_status.json?type=light

change type based on category