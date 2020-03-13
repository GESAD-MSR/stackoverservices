SELECT 
  Id, OwnerUserId, AcceptedAnswerId, 
  Tags, Score, AnswerCount, ViewCount,
  CommentCount, FavoriteCount, Title, Body,
  CreationDate, DeletionDate, ClosedDate 
  
  FROM `sotorrent-org.2019_06_21.Posts`
  WHERE Tags LIKE '%microservice%' 
