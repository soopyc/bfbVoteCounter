# News
The one and only bfbVoteCounter news channel! 

## Table of Contents
- [Breaking news](#breaking-news)
- [Smaller news](#corkboard)

## Breaking news
### Apr 3, 2020
Rewrite has started. The old script (currently in #master branch) is now deprecated due to messy code and large bug count, and speed.

## Corkboard
### Apr 6, 2020
Changed stuff:
```diff
- fullscreen mode (breaks code and disables scroll buffer in windows)
- colorama (using blessed, causes conflict when used together with colorama and blessed.)
+ more colors  (because why not?)
```

### Apr 5, 2020
Changed items:
```diff
+ --delete-logs parameter  (clear logs with not one, not two, but 10 clicks. Faster than deleting yourself :wink:)
+ better setup() 
+ blessed (supports more styling and underline and much much more.)
- blessings (no support on windows but i imagine most people using this thing will run windows so :P)
+ unintentional gitpod advertisement (https://github.com/kcomain/bfbVoteCounter/commit/927f3ab40eebc191074a053a99fdf56ae19da8fe)
```
