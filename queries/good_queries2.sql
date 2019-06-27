select word, sum(amount) as cun from dictionary where song in 
(select song from billboard
group by song)
group by word
order by cun desc;


select word, cun from 
(select word, count(*) as cun from dictionary where song in 
(select song from billboard
group by song)
group by word
order by cun desc) as t
where con < 100;



select song from billboard
group by song;


select word from 
(select word, sum(amount) as cun from dictionary where song in 
(select song from billboard
group by song)
group by word
order by cun desc) as t
where t.cun < 11;


select word from 
(select word, count(*) as cun from dictionary where song in 
(select song from billboard
group by song)
group by word
order by cun desc) as t
where t.cun < 100;

select song, count(*) from dictionary where word in
(select word from 
(select word, count(*) as cun from dictionary where song in 
(select song from billboard
group by song)
group by word
order by cun desc) as t
where t.cun < 100)
group by song;

select song, count(*) from dictionary
where word in (select word from 
(select word, sum(amount) as cun from dictionary where song in 
(select song from billboard
group by song)
group by word
order by cun desc) as t
where t.cun < 11)
group by song;


select song, count(*) as c from dictionary where word in
(select word from 
(select word, count(*) as cun from dictionary where song in 
(select song from billboard
group by song)
group by word
order by cun desc) as t
where t.cun < 100)
group by song;




select y, sum(c)/count(*) from 
(select year(week) as y, song from billboard
GROUP BY song, year(week)) as t
inner join 
(select song, count(*) as c from dictionary where word in
(select word from 
(select word, count(*) as cun from dictionary where song in 
(select song from billboard
group by song)
group by word
order by cun desc) as t
where t.cun < 100)
group by song) as j
on t.song = j.song
group by y;



select song, sum(101-position) as p from billboard group by song order by p desc;

select * from billboard where song = 45997;



select id, artist, t.song as song, rep, hw, ef, points, c from
(select
songss.id as id,
songss.artist as artist, 
songss.song as song,
songss.rep as rep,
songss.hard_words as hw,
songss.effective_size as ef,
sum(101-billboard.position) as points 
from billboard 
inner join songss 
on billboard.song = songss.id 
group by songss.id, songss.artist, songss.song
order by sum(101-billboard.position) desc) as t inner join
(select song, count(*) as c from dictionary where word in
(select word from 
(select word, count(*) as cun from dictionary where song in 
(select song from billboard
group by song)
group by word
order by cun desc) as t
where t.cun < 100)
group by song) as j
on t.id = j.song;



select y, sum(c)/count(*) from 
(select year(week) as y, song from billboard
GROUP BY song, year(week)) as t
inner join 
(select song, count(*) as c from dictionary where word in
(select word from 
(select word, count(*) as cun from dictionary where song in 
(select song from billboard
group by song)
group by word
order by cun desc) as t
where t.cun < 100)
group by song) as j
on t.song = j.song
group by y;





select
(round(2*rep, -1))/2 as rep,
hw,
(round(2*ef, -2))/2 as ef,
(round(2*c, -1))/2 as c,
avg(points) as points,
count(*) as count
from
(select id, artist, t.song as song, rep, hw, ef, points, c from
(select
songss.id as id,
songss.artist as artist, 
songss.song as song,
songss.rep as rep,
songss.hard_words as hw,
songss.effective_size as ef,
sum(101-billboard.position) as points 
from billboard 
inner join songss 
on billboard.song = songss.id 
group by songss.id, songss.artist, songss.song
order by sum(101-billboard.position) desc) as t inner join
(select song, count(*) as c from dictionary where word in
(select word from 
(select word, count(*) as cun from dictionary where song in 
(select song from billboard
group by song)
group by word
order by cun desc) as t
where t.cun < 100)
group by song) as j
on t.id = j.song
where t.rep > 10) as t
group by t.rep, t.hw, t.ef, t.c
order by points desc;

select j.y, round(100*t.c/j.c,2) from
(select y, 100*count(*) as c from
(select year(week) as y, week
from billboard
group by y, week) as t
group by t.y) as j
inner join
(select year(week) as y, count(*) as c
from billboard
group by y) as t
on t.y = j.y;


select year, count(*)
from maistocadas
group by year;

select 
songss.artist as artist, 
sum(101-billboard.position) as points 
from billboard 
inner join songss 
on billboard.song = songss.id 
group by songss.artist
order by sum(101-billboard.position) desc;

select year, avg(rep), count(*) as c from
(select year, maistocadas.song, rep from
maistocadas inner join
songss on
maistocadas.song = songss.id
where rep is not null) as t
group by year;



select t1.year, 
t1.avg_rep as avg_rep, 
t1.max_rep as max_rep, 
t1.min_rep as min_rep, 
t2.avg_rep as top_avg_rep,
t3.avg_rep as bottom_avg_rep,
t1.avg_hw as avg_hw, 
t1.max_hw as max_hw, 
t1.min_hw as min_hw, 
t2.avg_hw as top_avg_hw,
t3.avg_hw as bottom_avg_hw,
t1.avg_es as avg_es, 
t1.max_es as max_es, 
t1.min_es as min_es,
t2.avg_es as top_avg_es,
t3.avg_es as bottom_avg_es
from (
	select year, 
	avg(rep) as avg_rep, 
	max(rep) as max_rep, 
	min(rep) as min_rep, 
	avg(hw) as avg_hw, 
	max(hw) as max_hw, 
	min(hw) as min_hw, 
	avg(es) as avg_es, 
	max(es) as max_es, 
	min(es) as min_es
	from (
		select 
		year(billboard.week) as year, 
		songss.rep as rep, 
		songss.`hard_words` as hw, 
		songss.`effective_size` as es, 
		songss.id as id
		from  billboard
		inner join songss
		on billboard.song = songss.id
		where songss.rep > 5 and songss.effective_size > 145
		group by id, year) as t
	group by year
) as t1
inner join (
	select 
	year, 
	avg(rep) as avg_rep, 
	avg(hw) as avg_hw, 
	avg(es) as avg_es, 
	count(*)
	from (
		select @rank:=if(@prev_cat=t.year,@rank+1,1) as rank, 
		t.year, 
		t.rep, 
		t.hw,
		t.es,
		t.points,
		@prev_cat:=t.year
		from (
			select 
			year(billboard.week) as year,
			songss.rep as rep,
			songss.hard_words as hw,
			songss.effective_size as es,
			sum(101-billboard.position) as points 
			from billboard 
			inner join songss 
			on billboard.song = songss.id 
			group by songss.id, hw, es, songss.rep, year(billboard.week)
			order by year, sum(101-billboard.position) desc
		) t, (
			select 
			@rank:=0, 
			@prev_cat:=""
		)j
		where t.rep > 5 and t.es > 145
		order by t.year, t.points desc
	) temp
	where temp.rank <= 10
	group by year
) as t2
on t1.year = t2.year
inner join (
	select 
	year, 
	avg(rep) as avg_rep, 
	avg(hw) as avg_hw, 
	avg(es) as avg_es, 
	count(*)
	from (
		select @rank:=if(@prev_cat=t.year,@rank+1,1) as rank, 
		t.year, 
		t.rep, 
		t.hw,
		t.es,
		t.points,
		@prev_cat:=t.year
		from (
			select 
			year(billboard.week) as year,
			songss.rep as rep,
			songss.hard_words as hw,
			songss.effective_size as es,
			sum(101-billboard.position) as points 
			from billboard 
			inner join songss 
			on billboard.song = songss.id 
			group by songss.id, hw, es, songss.rep, year(billboard.week)
			order by year, sum(101-billboard.position)
		) t, (
			select 
			@rank:=0, 
			@prev_cat:=""
		)j
		where t.rep > 5 and t.es > 145
		order by t.year, t.points
	) temp
	where temp.rank <= 10
	group by year
) as t3
on t2.year = t3.year;

select y, count(*) as c from
(select year(week) as y, song from billboard group by y, song) as t group by y;

select y, count(*) as c from
(select year(week) as y, billboard.song, rep from billboard inner join songss on songss.id = billboard.song where rep is not null  group by y, billboard.song) as t group by y;



select t.y, t.c/j.c from
(select y, count(*) as c from
(select year(week) as y, song from billboard group by y, song) as t group by y) as j
inner join 
(select y, count(*) as c from
(select year(week) as y, billboard.song, rep from billboard inner join songss on songss.id = billboard.song where rep is not null  group by y, billboard.song) as t group by y) as t
on j.y = t.y;

select sum(gotten)/sum(aq_total) from
(
select t.year as year,
w.total_weeks*100 as total,
t.total as aq_total,
g.total as gotten,
100*g.total/t.total as perc
from
(select year(week) as year, count(*) as total
from billboard
group by year(week)) as t
inner join
(select year(week) as year, count(*) as total_weeks from (select week
from billboard
group by week) as t group by year(week)) as w
on t.year = w.year
inner join
(select year(billboard.week) as year, count(*) as total
from billboard
inner join songss
on billboard.song = songss.id
where songss.`source` is not null and songss.source != 0
group by year(billboard.week)) as g
on w.year = g.year) as t;

select year(billboard.week) as year, count(*) as total
from billboard
inner join songss
on billboard.song = songss.id
where songss.`source` is not null and songss.source != 0
#where songss.sourse is not null and songss.sourse != 0
group by year(billboard.week);


select ef, avg(points), count(*) from
(select
ef as ef,
points as points
from 
(select 
songss.artist as artist, 
songss.song as song,
`hard_words` as ef,
sum(101-billboard.position) as points 
from billboard 
inner join songss 
on billboard.song = songss.id 
where songss.rep > 5
group by songss.artist, songss.song, ef
order by sum(101-billboard.position) desc) as t) as t
group by ef;

select * from songss where song = 'around the world';

select * from songss where rep > 32 and rep < 34
order by effective_size;



select y, avg(ef) from
(select year(week) as y, effective_size as ef from billboard inner join songss on songss.id = billboard.song) as t
group by y;





select p.rank, p.y, p.s from
(select @rank:=if(@prev_cat=t.year,@rank+1,1) as rank, 
		t.year as y, 
		t.song as s,
		t.points as p,
		@prev_cat:=t.year
		from (
			select 
			year(billboard.week) as year,
			billboard.song,
			sum(101-billboard.position) as points 
			from billboard 
			inner join songss 
			on billboard.song = songss.id 
			group by songss.id, year(billboard.week)
			order by year, sum(101-billboard.position)
		) t)  as p where p.rank < 11;
		

select y, avg(c), count(*) from
(select y, s, ifnull(c, 0) as c, rank from
(select p.rank as rank, p.y as y, p.s as s from
(select @rank:=if(@prev_cat=t.year,@rank+1,1) as rank, 
		t.year as y, 
		t.song as s,
		t.points as p,
		@prev_cat:=t.year
		from (
			select 
			year(billboard.week) as year,
			billboard.song,
			sum(101-billboard.position) as points 
			from billboard 
			inner join songss 
			on billboard.song = songss.id 
			where songss.text is not null
			group by songss.id, year(billboard.week)
			order by year, sum(101-billboard.position) desc
		) t) as p where p.rank < 11) as p left join 
(select song, count(*) as c from dictionary
where word in (select word from 
(select word, sum(amount) as cun from dictionary where song in 
(select song from billboard
group by song)
group by word
order by cun desc) as t
where t.cun < 11)
group by song) as t
on p.s = t.song) as t group by y;

select y, avg(c), count(*) from
(select y, s, ifnull(c, 0) as c, rank from
(select p.rank as rank, p.y as y, p.s as s from
(select @rank:=if(@prev_cat=t.year,@rank+1,1) as rank, 
		t.year as y, 
		t.song as s,
		t.points as p,
		@prev_cat:=t.year
		from (
			select 
			year(billboard.week) as year,
			billboard.song,
			sum(101-billboard.position) as points 
			from billboard 
			inner join songss 
			on billboard.song = songss.id 
			where songss.text is not null
			group by songss.id, year(billboard.week)
			order by year, sum(101-billboard.position)
		) t) as p where p.rank < 11) as p left join 
(select song, count(*) as c from dictionary
where word in (select word from 
(select word, sum(amount) as cun from dictionary where song in 
(select song from billboard
group by song)
group by word
order by cun desc) as t
where t.cun < 11)
group by song) as t
on p.s = t.song) as t group by y;


select song, count(*) as c from dictionary
where word in (select word from 
(select word, sum(amount) as cun from dictionary where song in 
(select song from billboard
group by song)
group by word
order by cun desc) as t
where t.cun < 11)
group by song;

select c as pp, avg(p) as p, count(*) as c from
(select j.song as s, p, ifnull(c, 0) as c from
(select billboard.song as song, sum(101-position) as p 
from billboard inner join songss 
on billboard.song = songss.id where songss.text is not null group by song) as j left join
(select song, count(*) as c from dictionary
where word in (select word from 
(select word, sum(amount) as cun from dictionary where song in 
(select song from billboard
group by song)
group by word
order by cun desc) as t
where t.cun < 11)
group by song) as t on j.song = t.song) as t group by c;






select year(week) as y, billboard.song as song from billboard inner join songss on billboard.song = songss.id where songss.text is not null group by y, song;





