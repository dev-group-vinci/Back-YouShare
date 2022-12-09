DROP SCHEMA IF EXISTS youshare CASCADE;
CREATE SCHEMA youshare;


create table youshare.users
(
    id_user  serial                primary key,
    username varchar(60)          not null,
    role     varchar(10)            not null default 'user' CHECK (role = 'admin' or role = 'user'),
    email    varchar(128)          not null unique ,
    password char(60)              not null,
    biography varchar(200)         null

);

create table youshare.posts
(
    id_video serial                primary key,
    id_user  integer               not null,
    id_url   char(11)              not null,
    state    varchar(9)            not null default 'published' CHECK (state = 'published' or state='deleted'),
    date_published    TIMESTAMP not null default CURRENT_TIMESTAMP,
    date_deleted      TIMESTAMP ,
    text varchar(280) not null,
    FOREIGN KEY (id_user) REFERENCES youshare.users (id_user),
);

create table youshare.shares
(
    id_user integer not null,
    id_video integer not null,
    FOREIGN KEY (id_user) REFERENCES youshare.users (id_user),
    FOREIGN KEY (id_video) REFERENCES youshare.posts (id_video),
    PRIMARY KEY (id_user,id_video)
);

create table youshare.likes
(
    id_user integer not null,
    id_video integer not null,
    FOREIGN KEY (id_user) REFERENCES youshare.users (id_user),
    FOREIGN KEY (id_video) REFERENCES youshare.posts (id_video),
    PRIMARY KEY (id_user,id_video)
);

create table youshare.comments
(
    id_comment serial primary key,
    id_user integer not null,
    id_video integer not null,
    id_comment_parent integer,
    text varchar(280) not null,
    state    varchar(9) not null default 'published' CHECK (state = 'published' or state='deleted'),
    date_published    TIMESTAMP not null default CURRENT_TIMESTAMP,
    date_deleted      TIMESTAMP ,
    FOREIGN KEY (id_user) REFERENCES youshare.users (id_user),
    FOREIGN KEY (id_video) REFERENCES youshare.posts (id_video),
    FOREIGN KEY (id_comment_parent) REFERENCES youshare.comments (id_comment)
);

create table youshare.friendships(
    id_friendship serial primary key ,
    id_asker integer not null,
    id_receiver integer not null,
    date timestamp not null default CURRENT_TIMESTAMP,
    state varchar(8) not null default 'pending' CHECK (state='pending' or state='accepted' or state='refused'),
    FOREIGN KEY (id_asker) REFERENCES youshare.users (id_user),
    FOREIGN KEY (id_receiver) REFERENCES youshare.users (id_user)
);