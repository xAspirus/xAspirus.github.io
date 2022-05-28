---
title: /board
created: '2022-05-14T14:11:41.420Z'
modified: '2022-05-16T12:00:19.470Z'
---

# /board

/board is a image board made using flask and sqlite3.
It is written in python and it source is available on [github/board](https://github.com/xAspirus/board).

### Boards
A board is a list of posts. It has a name.

### Posts
A post is a user-submitted text document. It has the author's username and date of submission.

### User
A user is a member of the website.

Users can have the following roles:

#### Admin
Users with this role can delete any posts.

#### Normal
Users with this role can delete their own posts.

#### Banned
Users with this role cannot submit any posts. But they can still view posts.


### Database
```
users = [
          [
            username:  ,
            email:     ,
            password:  ,
            role:     Possible(1: Admin, 0: Normal, -1: Banned)  ,
          ]  , more users...
        ]

boards = {
board_name: "all":  [         
             post_id: [
                        author: username                       ,
                        date: unix timestamp (server side)     ,
                        content: "Markdown Formatted Content"  ,
                      ]  ,
             post_id: [
                        author: removed                        ,
                        date: 0                                ,
                        content: "deleted"                     ,
                      ]  , more posts...
                    ]  , more boards...
         }
```

### Image Board API
```

/b/all?count=10?offset=0
returns: list of posts

/b/all/180
returns: post with id 180

/b/all/post
post: content into board


```

