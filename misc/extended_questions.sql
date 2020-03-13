SELECT
   p.Id as Id,
   i.Type as Type,
   p.OwnerUserId as OwnerUserId,
   p.AcceptedAnswerId as AcceptedAnswerId,
   p.Tags as Tags,
   p.Score as Score,
   p.AnswerCount as AnswerCount,
   p.ViewCount as ViewCount,
   p.CommentCount as CommentCount,
   p.FavoriteCount as FavoriteCount,
   p.Title as Title,
   p.Body as Body,
   p.CreationDate as CreationDate,
   p.DeletionDate as DeletionDate,
   p.ClosedDate as ClosedDate
FROM [sotorrent-org:2019_06_21.Posts] as p
INNER JOIN [sotorrent-org:2019_06_21.PostType] as i
ON p.PostTypeId = i.Id
WHERE Tags LIKE '%microservice%'
