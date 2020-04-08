# Corkboard 
Smaller/minor news
### Apr 8, 2020
```diff
+ --quiet param
= updated --output-interval (was --debug-interval)
+ whitespaces
- useless 0
+ updated colors
+ prompts user that config is capital letter and will not be able to be used in counting
+ better formatting
+ changed shiny counting to embed in voters (speed things up by a few magnitudes)
+ display better stats
+ allows the script to be imported, but prompts the user not to use it when they don't know what they're doing.
! release candidate.
```

### Apr 7, 2020
```diff
! `Video` object and `Comment` object output their title and comment text respectively 
+ Counting method
+ dumps comments just like the old one
+ argument groups (looks so so so so so much better)
+ emergency dump
```

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

[Go back](../news)
