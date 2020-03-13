SELECT
   p.Id as Id,
   i.Type as Type,
   p.OwnerUserId as OwnerUserId,
   p.ParentId as ParentId,
   p.Score as Score,
   p.CommentCount as CommentCount,
   p.Body as Body,
   p.CreationDate as CreationDate,
   p.DeletionDate as DeletionDate
FROM `sotorrent-org.2019_06_21.Posts` as p
INNER JOIN `sotorrent-org.2019_06_21.PostType` as i
ON p.PostTypeId = i.Id
