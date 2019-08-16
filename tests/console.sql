USE my_database;
SELECT * FROM test ORDER BY Name;

DROP TABLE news;
CREATE TABLE news (ID INT NOT NULL);

SELECT n.Name as name, COUNT(news.link) as count
    FROM names as n
    JOIN news ON n.ID = news.ID
    GROUP BY news.ID
    ORDER BY count DESC;

SELECT news.headline as headline, news.link as link
    FROM news
    JOIN names ON names.ID = news.ID
    WHERE names.Name LIKE 'Troutman%';

SELECT n.Name as name, news.*
    FROM names as n
    JOIN news ON n.ID = news.ID
    WHERE name LIKE 'DLA%' OR name LIKE 'Dentons%';

SELECT n.Name as name, news.headline as headline, news.link as link FROM names as n JOIN news ON n.ID = news.ID ORDER BY name;

