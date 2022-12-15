-- Insertion users
INSERT INTO youshare.users(role,username,email,password,biography,picture) VALUES ('user','Rayan','rayan@gmail.com','$2b$10$S7q3Bh2YbmTBnkf2gqjHjOfIFSa8QbAM80tgWbKt7OWLl8l.NN2CG','Rust ?','15-12-2022-17:59:326d17cb3d-db1a-4d6b-8190-d979d88b606c.jpg');
INSERT INTO youshare.users(role,username,email,password,biography,picture) VALUES ('user','Mehdi','mehdi@gmail.com','$2b$10$DYQl4ZD2wcXdOst.9KBPZuXA3KnbKqzlTm9MpqiRVLvWyrYfFeP4S','LoL ?','15-12-2022-17:55:5661f8ebb5-c275-4b6d-afad-2dfe330dcc6d.jpg');
INSERT INTO youshare.users(role,username,email,password,biography) VALUES ('admin','Zoe','zoe@gmail.com','$2b$10$XdK1Q5zF3OF9jhcxKW.fbuyu6pR7DxIJXPWKwmhFPfVbPVDVcV.7q','Basic fit ?');
INSERT INTO youshare.users(role,username,email,password,biography) VALUES ('user','Loic','loic@gmail.com','$2b$10$Ka0DPV24xZziK2S8Wxiy1u/0/CFwKV4BNfpCpEOnnZvys6x0xbKlK','Un verre ?');
INSERT INTO youshare.users(role,username,email,password,biography) VALUES ('user','Eliott','eliott@gmail.com','$2b$10$LHN9wSsLomTaLf.cCBJe6ObQk9ra4j8LhA.uQyqypOq8M2C0LJadG','Une piscine ?');

-- Insertion amis
INSERT INTO youshare.friendships(id_asker,id_receiver,state,date) VALUES (1,2,'accepted','2022-12-14 23:54:36.032430');
INSERT INTO youshare.friendships(id_asker,id_receiver,state,date) VALUES (4,1,'accepted','2022-12-14 23:54:36.032430');
INSERT INTO youshare.friendships(id_asker,id_receiver,state,date) VALUES (3,4,'accepted','2022-12-14 23:54:36.032430');
INSERT INTO youshare.friendships(id_asker,id_receiver,state,date) VALUES (5,1,'refused','2022-12-14 23:54:36.032430');
INSERT INTO youshare.friendships(id_asker,id_receiver,state,date) VALUES (5,2,'pending','2022-12-14 23:54:36.032430');


-- Insertion posts

INSERT INTO youshare.posts(id_user,id_url,text,state,date_published) VALUES (1,'aLcCTHXh86I','Des nouilles ?','published','2022-12-11 17:52:36.85');
INSERT INTO youshare.posts(id_user,id_url,text,state,date_published) VALUES (1,'jVZdW0sV_0Y','Upgrade votre pc toujours utile ?','published','2022-12-14 19:31:09.212657');
INSERT INTO youshare.posts(id_user,id_url,text,state,date_published) VALUES (3,'IreuIfCLAk8','Une journée dans ma peau','published','2022-12-14 03:23:09.920242');
INSERT INTO youshare.posts(id_user,id_url,text,state,date_published) VALUES (3,'Qaqi2jbu1YU','Le permis trop dur','published','2022-12-13 14:35:30.082');
INSERT INTO youshare.posts(id_user,id_url,text,state,date_published) VALUES (4,'TaAM5MovXp0','Mon petit Jamy et les frites ❤','published','2022-12-12 14:14:55.544');
INSERT INTO youshare.posts(id_user,id_url,text,state,date_published) VALUES (4,'-C66XErGQoQ','Un peu de danse ça fait toujours plaisir','published','2022-12-14 19:04:37.893');

-- Insertion des likes

INSERT INTO youshare.likes(id_user,id_post) VALUES (2,1);
INSERT INTO youshare.likes(id_user,id_post) VALUES (3,1);
INSERT INTO youshare.likes(id_user,id_post) VALUES (4,1);
INSERT INTO youshare.likes(id_user,id_post) VALUES (3,2);
INSERT INTO youshare.likes(id_user,id_post) VALUES (4,2);
INSERT INTO youshare.likes(id_user,id_post) VALUES (1,3);
INSERT INTO youshare.likes(id_user,id_post) VALUES (2,4);
INSERT INTO youshare.likes(id_user,id_post) VALUES (1,6);
INSERT INTO youshare.likes(id_user,id_post) VALUES (2,6);
INSERT INTO youshare.likes(id_user,id_post) VALUES (5,6);

-- Insertion des shares

INSERT INTO youshare.shares(id_user,id_post) VALUES (2,1);
INSERT INTO youshare.shares(id_user,id_post) VALUES (3,1);
INSERT INTO youshare.shares(id_user,id_post) VALUES (4,1);
INSERT INTO youshare.shares(id_user,id_post) VALUES (4,2);
INSERT INTO youshare.shares(id_user,id_post) VALUES (1,3);
INSERT INTO youshare.shares(id_user,id_post) VALUES (2,4);
INSERT INTO youshare.shares(id_user,id_post) VALUES (1,4);
INSERT INTO youshare.shares(id_user,id_post) VALUES (2,5);
INSERT INTO youshare.shares(id_user,id_post) VALUES (1,6);
INSERT INTO youshare.shares(id_user,id_post) VALUES (2,6);
INSERT INTO youshare.shares(id_user,id_post) VALUES (5,6);

-- Insertion des commentaires

INSERT INTO youshare.comments(id_post,id_user,text,state,date_published) VALUES (1,3,'Ça à l’air trop bon !!!','published','2022-12-11 18:31:23.85');
INSERT INTO youshare.comments(id_post,id_user,text,state,date_published) VALUES (1,2,'Ces nouilles sont vraiment pas chers en plus, j’en ai commandé une caisse','published','2022-12-11 19:13:14.85');
INSERT INTO youshare.comments(id_post,id_user,text,state,date_published) VALUES (3,1,'Oh je suis dans la vidéo !!!!','published','2022-12-14 07:23:09.920242');
INSERT INTO youshare.comments(id_post,id_user,text,state,date_published) VALUES (6,1,'J’aime beaucoup cette chorée','published','2022-12-14 20:40:27.893');
INSERT INTO youshare.comments(id_post,id_user,text,state,date_published,date_deleted) VALUES (6,1,'Oh les fiaks','deleted','2022-12-15 20:04:37.8','2022-12-14 10:59:37.45');
INSERT INTO youshare.comments(id_post,id_user,text,state,date_published) VALUES (6,2,'Intéressant 🤩','published','2022-12-14 21:54:56.2');
INSERT INTO youshare.comments(id_post,id_user,text,state,date_published) VALUES (6,4,'Jennie !!! je suis trop fan !!!!','published','2022-12-14 20:04:17.3');