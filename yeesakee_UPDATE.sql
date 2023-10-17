UPDATE business set numcheckins = 
(SELECT checkin_count FROM check_in where bid = business.bid)

UPDATE business set review_count = 
(SELECT COUNT(*) FROM reviews where bid = business.bid)

UPDATE business set reviewrating = 
(SELECT AVG(stars) FROM reviews where bid = business.bid)