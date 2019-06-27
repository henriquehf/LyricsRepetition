
set @tbs := (select count(*) from (select count(*) from songss inner join billboard on songss.id = billboard.song group by songss.id) as t);
set @tbr := (select count(*) from billboard);


# constructs graph song% X billboard%
select 
@number := @number + 1,
@total_amount := @total_amount + amount,
(@number/@tbs)*100 as songs_percent,
(@total_amount/@tbr)*100 as rankings_eprcent
from 
(SELECT @number := 0, @total_amount := 0) AS dummy
cross join
(select 
songss.id as id,
count(*) as amount
from billboard 
inner join songss 
on billboard.song = songss.id 
group by billboard.song
order by amount desc) as j;

#artists by popularity
select 
songss.artist as artist, 
sum(101-billboard.position) as points 
from billboard 
inner join songss 
on billboard.song = songss.id 
group by songss.artist
order by sum(101-billboard.position) desc;

#songs by popularity
select 
songss.artist as artist, 
songss.song as song,
sum(101-billboard.position) as points 
from billboard 
inner join songss 
on billboard.song = songss.id 
group by songss.artist, songss.song
order by sum(101-billboard.position) desc;

#graph % per year
select t.year as year,
w.total_weeks*100 as total,
t.total as aq_total,
g.total as gotten
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
where songss.sourse is not null and songss.sourse != 0
group by year(billboard.week)) as g
on w.year = g.year;

#% each sourse
select t.sourse, 100*(t.count/j.count)
from
(select sourse, count(*) as count
from songss
where sourse is not null
group by sourse) as t
join
(select count(*) as count
from songss
where sourse is not null) as j;

#songs ordered by popularity and year 
select 
year(billboard.week) as year,
songss.artist as artist, 
songss.song as song,
sum(101-billboard.position) as points 
from billboard 
inner join songss 
on billboard.song = songss.id 
group by songss.artist, songss.song, year(billboard.week)
order by year, sum(101-billboard.position) desc;



# % os mais tocadas lyrics gotten
select t.year, 100*j.count/t.count from
(select year, count(*) as count from maistocadas group by year) as t
inner join
(select year, count(*) as count from maistocadas inner join songss on maistocadas.song = songss.id where songss.text is not null group by year) as j
on t.year = j.year;

# return the average metrics for the top X most popular songs from each year
select 
year, 
avg(rep), 
avg(hw), 
avg(es), 
count(*)
from (
	select @rank:=if(@prev_cat=t.year,@rank+1,1) as rank, 
	t.year, 
	t.rep, 
	t.hw,
	t.es,
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
	order by t.year, t.rep desc
) temp
where temp.rank <= 10
group by year;

# return the average metrics for the loest X most popular songs from each year, excluding those with probably no lyrics
select 
year, 
avg(rep), 
avg(hw), 
avg(es), 
count(*)
from (
	select @rank:=if(@prev_cat=t.year,@rank+1,1) as rank, 
	t.year, 
	t.rep, 
	t.hw,
	t.es,
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
	where t.rep > 5
	order by t.year, t.rep
) temp
where temp.rank <= 10
group by year;


# returns avg, max and min of all metrics, per year, with avg of most and least popular as well
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

#histogram
select rep, avg(points) from
(select
(round(2*rep, -1))/2 as rep,
points as points
from 
(select 
songss.artist as artist, 
songss.song as song,
songss.rep as rep,
sum(101-billboard.position) as points 
from billboard 
inner join songss 
on billboard.song = songss.id 
where songss.rep > 5 and songss.effective_size > 145
group by songss.artist, songss.song, rep
order by sum(101-billboard.position) desc) as t) as t
group by rep;


#least used words
select song, count(*) from dictionary
where word in (select word from 
(select word, sum(amount) as cun from dictionary where song in 
(select song from billboard
group by song)
group by word
order by cun desc) as t
where t.cun < 11)
group by song;




#palavras menos usadas (aparece em menos musicas)
select y, sum(c) from 
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


#retorna todas as metricas por música
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



#histograma de 4 dimenções
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











#graficos usados:

#porcentagem de rankings coletados billboard
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
#porcentagem de rankings coletados maistocadas
select year, count(*)
from maistocadas
group by year;


