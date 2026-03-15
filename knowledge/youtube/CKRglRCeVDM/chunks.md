# Chunks

## Chunk 01
Has anyone checked in on Amazon lately?
Because five or so years ago, all the
course bros were selling Amazon FBA
passive income courses. A couple of them
went to jail. Most of them have gone out
of business. But guess what? Amazon's a
trillion dollar company. They're still
doing great. And there's still countless
people making millions of dollars a year
selling stuff on Amazon that they're

## Chunk 02
just drop shipping from China or
importing from China and shipping it
directly to an Amazon warehouse. So
today, I'm going to show you how to
scrape Amazon, find the best sellers,
find the products that are about to be
best sellers, and just to find the most
opportunity to compete because most
people when they go to sell something on
Amazon, they're just picking things that

## Chunk 03
they're comfortable with or familiar
with. But not today. We're going to use
hard facts and data to find winning
products in three different categories:
pets, household items, and books and
education. This is a banger of a video,
so let's dive right in.
Okay, the first category I'm going to
scrape today is pet accessories, as in
anxiety beds, calming vest, puzzle

## Chunk 04
feeders, interactive toys, all the types
of stuff that Americans spend way too
much money on. Okay, so I'm logged into
OxyLabs, which is the tool I use to
scrape. If you go to Oxyabs.io/cris,
you can get both a free trial and 20%
off any scraping credits. Okay, so I'm
logged into OxyLabs and I'm going to
click on web scraper API over here on
the left and then I'm going to click

## Chunk 05
explore API playground. Okay, now here
on this dropown I'm going to go to
Amazon. Then under scraper I'm going to
click best sellers. Okay, now it's
asking for the browse node ID. Don't
freak out. Here's what I'm going to do
to get this. You can go to Grock, Chad
Gupt, Claude, whatever you want to do.
Any of the AIS I'm going to use Claude.
I already have the categories that I'm

## Chunk 06
interested in. And so my prompt is right
here. I'm going to scrape Amazon
bestsellers, but I need the five to
sevendigit query code for each of the
below categories. What are they? And by
the way, I'm pasting the outputs of this
prompt into Google Docs, and I'm putting
that link in the show notes below
without any payw wall. I don't need your
email address or anything. Just use that

## Chunk 07
for free. That way, you can skip this
step entirely. Boom. Look at that. Gave
me a spreadsheet. You're going to go to
this spreadsheet that I'm providing in
the show notes below right here. And I'm
just going to pick one. I want to look
up pet accessories. So, I'm going to
copy that one. Boom. Go back here. Paste
that. Okay. Now, parsing needs to be
true. This just means I want it to give

## Chunk 08
me structured data and not unstructured
data because I don't even know what
parsing means. I want it to be able to
go in a spreadsheet so I can read it.
Domain, I'm going to choose.com because
I'm in the US. If you're in the UK or a
different country, then pick your own
respective domain. It would be
interesting regardless of what country
you're in to scrape the same thing in

## Chunk 09
different countries and compare contrast
the prices of the same bestsellers. That
could be a whole other video. And then
very important that you choose local.
This is where your VPN is or where the
scraper thinks that you're located. If I
don't pick this and it uses a VPN in say
the Philippines, then it's going to
return best sellers from the Philippines
and in the Filipino pesos. So you're

## Chunk 10
going to pick whatever currency of
whatever country that you want these
prices to be displayed in. So I'm going
to go United States English. Okay. Now,
on location, I'm just going to put in a
zip code near me and submit request.
Boom. Took about 10 seconds. We're done.
I can see over here on the right the
preview. I can see it's showing the
delivery location based on the zip code

## Chunk 11
that I entered. It looks like it scraped
about 50 items, which is awesome. I'm
going to click export results and then
JSON. I don't know what a JSON is or how
to read that data. So, I'm going to go
back to Claude over here. I'm going to
upload that JSON file and I'm going to
say
convert this to CSV data and make the
Amazon URLs complete and clickable

## Chunk 12
because I've done this before and it
gives me the URL suffixes, the endings,
but it doesn't include ww.amazon.com.
I want to be able to click it directly
from Google Sheets. So, simple request
for cloud. There's the export. We're
going to download it. And then I really
want to put it in a Google sheet. So,
I'm going to open a blank Google sheet.
I'll also include this in the show

## Chunk 13
notes. I'm going to paste it. Boom.
There it is. Number of ratings. That
column is irrelevant. Price, currency,
the rating on a fivestar scale, the
title of the product, the price. Again,
we'll delete that cuz it's redundant.
The ASIN, which is the Amazon standard
identification number, and then the URL
so we can click on it. So, this is
incredible. I'm going to delete this

## Chunk 14
column because we don't need that. I
want to see the ratings and the ratings
count. I'm going to drag this over to be
next to that. I want to see more of the
title. And let's just look at one of
these. 8,800 ratings. Bags for a cat
feeder. Okay, cool. Okay, now you may be
wondering like, in what order were these
scraped? We got 50 results. They're
ordered in column A 1 through 50. What

## Chunk 15
does that even mean? Well, it means in
that specific category with that
specific 8 or so digit code that I
uploaded for pet accessories, these are
the best selling products in that one
specific category. But what do we do
with that data? Well, there's a few
things. For starters, we want to look
for a review count and sales rank
mismatch. This is the single most

## Chunk 16
valuable signal that most people miss.
If a product has a very good or
highseller rank, but a low review count
of like under 300, say, it means that
the market is buying. The market loves
this product, but it's not a lockeddown
category yet. Nobody really owns it,
right? It's not the McDonald's of the
burger franchises yet. That means
there's still opportunity for you to

## Chunk 17
swoop in and sell a competing product to
capture that first place position. BSR
equals bestseller rank. So high BSR plus
high review count equals established
market leader. That's already kind of
saturated. We're going to ignore those.
But high BSR plus low review count
equals a land grab is still in progress.
It means this is still up for the taking
for you. So let's do some easy division

## Chunk 18
real quick to find what those products
are. that show the most opportunity. How
do we do that? Very simple. We're going
to add a new column. We're going to say
equals. Click on the ratings count and
divide it by the bestseller rank for
this category. Boom. Click the check
box. We don't want this as a monetary
number. We want this just as a number.
Now, we are going to filter and sort A

## Chunk 19
to Z. Let's add a couple decimal points
here. So this product is the 40th
bestselling product in the category, but
it only has five ratings. Interesting.
So according to this scrape and
according to this logic, this could be
the biggest opportunity in this
category. Now, this is just one way of
looking at the opportunity here. This is
not the end- all beall. I'm going to

## Chunk 20
cover a lot more strategies or tactics
for finding winning products. This is
just one. So before you go invest your
life savings in an automatic cat feeder,
just wait. There's more to this story.
Now, if you see here, the least amount
of opportunity is on the best seller in
the category because it already has 8800
reviews. And the percentage of people
that actually leave a rating or review

## Chunk 21
on an Amazon product can vary between 1
and 5%. Let's say it's 1%. Well, we need
to take this 8800 number and multiply it
by 100. So that's 880,000.
It says 6,000 people bought this in the
last month. So if this product has been
for sale for like 12 years, then that
number would be accurate. It's probably
more like 2% of people buying this or
leaving review, which means we would

## Chunk 22
have to multiply that 8,800 by 50 and we
get about 440,000,
which means that one person made
millions of dollars selling this one
product on Amazon, which is kind of
wild. But we don't care about this one.
It's already oversaturated. And you know
what? this one here at the very top.
This might not be enough opportunity.
You can't automatically assume that this

## Chunk 23
is the best opportunity in the pet beds
or accessories category. There's more to
the story that we're going to cover. So,
I want to find outliers. Now, how do you
do that? Well, I'm going to sort them
from 1 to 50 again, how they were
originally, and just look for outliers
in column F, the count of the ratings.
Okay, boom. The top six all have
thousands, if not tens of thousands of

## Chunk 24
ratings, but number four here only has
727,
which is very, very interesting. And
number 11 here has only 463. So you can
see these are outliers. And an easy way
for spotting these outliers is to go
highlight the column, click format,
conditional formatting, color scale.
Click that. Click that. Actually, we're
going to click that. And we're going to

## Chunk 25
look for the green. We're going to look
for the green cells that are near the
top of this list because we have them
sorted from number one to number 50th
best seller. So, what's standing out?
This product, this product, this
product, and then some of these. Now,
down here, these are dark green, which
is great, but they're also not very
highly ranked as best sellers. So,

## Chunk 26
you're just going to have to do your own
research on that. Now you can start to
use your beautiful brain to find reasons
why this one number four is an outlier.
Okay, so we'll click on it here. What's
different about this? Well, first of
all, why don't we ask Claude? I'm going
to screenshot this. And then I'm going
to go to the other top four. Screenshot
this. Screenshot that. Boom. And then

## Chunk 27
screenshot number one. Now I'm going to
screenshot the top four in the
spreadsheet. I'm going to go back to
Claude. I'm going to add all five of
those screenshots to my chat window and
say, now keep in mind, I'm going to try
a different prompt where I say which one
of these top four show the most
opportunity to copy. I'm going to do
that in two different windows and see if

## Chunk 28
I'm right because I want to learn
different things here. In one, I want to
tell Claude my hypothesis so it can
confirm or deny that hypothesis or tell
me reasons why my hypothesis might be
true. And in the other one, I want it to
tell me in an unbiased way which of the
top four are showing the best
opportunity to copy with a competing
product. So, let's start with this. Now,

## Chunk 29
let's go to a different cloud window.
While we wait for that one to spit out,
upload the same five screenshots.
My prompt, which one of these four
products show the best opportunity for
me to compete with directly and why? I
want to import a similar product from
Alibaba and sell it on Amazon. Okay, so
with the first prompt, it said, "Great
eye, Chris." Here's what jumps out. I'm

## Chunk 30
not going to read this verbatim. You can
pause it and read it, but it says number
four is doing so well because the
twoin-one angle is doing the heavy
lifting. It's the only product in the
top four that bundles a food feeder and
water dispenser together. That's
amazing. Now, I could have looked at it
myself with my own two eyes and learned
that, but this is better. This is

## Chunk 31
faster. And it's going to find other
things that I certainly would have
missed cuz my attention to detail is
absolutely terrible. Highest rating with
fewest reviews. Now, that's something
that I did pick out, but remember that's
only one angle here. Gravityfed equals
zero complexity. No Wi-Fi, no app, no
voice recorder, no batteries. It's
simplicity means fewer returns, fewer

## Chunk 32
negative reviews about stop working or
app won't connect. Amazon's algorithm
rewards low return rates. This is
amazing. A lot of times we think that
consumers want all the features, all the
tech, everything. But if it has all that
stuff, maybe we do want it. But if it
has all that stuff, that means there's a
higher likelihood that people will
return that problem due to defects. And

## Chunk 33
then Amazon's algorithm knows, wo, 3% of
people are returning this one, whereas
only 1% of people are returning that
one. So when people search cat feeder on
Amazon, we're going to rank the one that
people are returning less of much higher
because Amazon doesn't make money when
we return stuff and neither does the
seller. And then it also says pricing,
the $29.99 sweet spot. It matches number

## Chunk 34
two exactly, but delivers more perceived
value. Two products verse one. I'm like
chuckling to myself because I'm like
convincing myself to go start importing
cat features, but I promise I won't.
Someone watching this can. Meanwhile,
number three is 50 bucks and Amazon is
literally flagging it as price higher
than typical. Review velocity matters
more than review count. Okay, number one

## Chunk 35
isn't even a feeder. Okay, the top
seller is almost certainly an Alibaba
importer. generic brand name sold by
third party fulfilled by Amazon. This is
Okay, so if you're sourcing a competitor
from Alibaba, the gravity fed two in one
design is dead simple to manufacture.
It's basically two plastic containers
with gravity flow. Okay, so now we got
to go find a product just like this on

## Chunk 36
Alibaba. Okay, here's what we're going
to do. We're going to go back to Oxyabs.
We're going to go website Alibaba
scraper Alibaba. Search term automatic
cat feeder water dispenser twoin-1
gravity. Okay, then we're going to click
submit request. Much easier than even
the Amazon scraper. Also, in case you're
wondering, anytime you're scraping on
OxyLabs, you don't have to worry about

## Chunk 37
Amazon, Alibaba, or any of those
companies blocking you because Oxyabs is
able to bypass all of these
anti-scraping measures that a lot of
these tech companies have. It's got over
177 million IP addresses that it rotates
between to protect you. Boom. All right,
there's the results. We're going to
click export results. JSON response.
Gonna go back to Claude. Boom. Add

## Chunk 38
photos and files. Make this a CSV. Now,
while it's doing that, we're going to go
to the other Claude prompt where I
basically said, "Hey, in an unbiased
way, which of these four products shows
the most opportunity?" And wouldn't you
guess it, product number four is the one
that it chose. Lowest barrier to entry,
still selling well, simplest to
manufacture, better margin potential.

## Chunk 39
That's one thing we really have to look
at. I almost forgot. There's a chance
that number four here, this beloved
twoin- one gravity feeder, has low
margins. Like, what if you have to pay
$20 and sell it for 30 and after fees
and shipping and all that, you don't
make any money? That could be the case.
We'll find out here in a minute. Oo, I
like that Claude says easy to

## Chunk 40
differentiate. The listing says plastic.
You could come in with a slightly
upgraded version. Stainless steel bowls,
better seal design, include a mat, and
immediately position above them.
Beautiful. While we're waiting for
Claude to spit out that spreadsheet
version, we're going to go do this the
more low tech way. We go to alibaba.com.
Right there. Boom. Image search. So, we

## Chunk 41
go back to this lovely product of ours
and we're going to save the image and
we're going to search Alibaba by that
image. All right, guys. I'm not going to
lie, there's a lot of really similar
looking products here. Twoin one
automatic food and water feeding bowl.
$3.89.
It's got the water on the left, the food
on the right. Look at this one. Water on

## Chunk 42
the left, food on the right. The only
difference is this one has black P
plastic around the water. This one's
clear. I think the clear looks better.
Honestly, you can see the water level
more easily. I mean, this is a $3
product that's selling for $30 on
Amazon. This one's $155. If you order a
100 pieces, in case you're not doing the
math, that's only $150 worth of product.

## Chunk 43
Of course, shipping is going to add a
lot to that, but not as much as you'd
think. And that's coming from someone
that's been ordering millions of dollars
worth of electronics and other items
from Alibaba and AliExpress for the last
17 years. So, let's look at this one
here. $155. You can see the levels of
each. It's gravityfed 2in1. This is
amazing. If you want it in black, I

## Chunk 44
could just reach out and say, "Hey, I
want this in black." Surely they're
already making it in black. So, it looks
like this is 30x 30x 30 cm, which is
give or take like 10 to 12 in of each of
the three dimensions. 1 kilogram, which
is 2.2 lb. So, if I were to order a
hundred of these for $155 total, keep in
mind, I don't need to ship it to myself.
I can ship it directly to an Amazon

## Chunk 45
warehouse and they will take it from
there and ship it out to all of their
other warehouses. So for seaf freight
and like 30% tariffs, you're probably
looking at about four to five dollar per
unit just to get it from China to
Amazon. Let's say five to be
conservative. Let's say these are $2 per
unit instead of $1.50 to be
conservative. That's $7 landed to an

## Chunk 46
Amazon warehouse. But Amazon's going to
take a cut per unit sold. Because of the
dimensions of this item, it pushes you
past what Amazon calls its large
standard size category and into their
large bulky category, which means you're
going to pay between $10 and $15 in
Amazon fees. That includes everything.
It includes their shipping from Amazon
to the consumer. Everything, storage,

## Chunk 47
and all that. So, your total fees, cost,
imports, tariffs, taxes, everything per
unit sold is going to be between $16 and
$21, leaving you a net profit of $9 per
unit if you sell it at the same price as
these other guys, which is a 30% net
profit margin, 30%. Which is really,
really good for Amazon. That's like what
Amazon FBA fulfilled by Amazon sellers
used to make 5 to 15 years ago. And it's

## Chunk 48
only possible because of this research
that we're doing. Most people when
they're selling on Amazon, they just
find a category that they like. Like I
like going to the gym. Chris like gym.
Chris imports. And so everyone's
importing gym equipment or supplements
or clothing, shoes, whatever. Buy with
data, sell with emotion. That's a
Shannon Gene quote. Now, if we really

## Chunk 49
want to get good with this, we'll order
a slightly smaller version to get us
away from that bulky category and into
the large category. that would save us
like $3 a unit. So, if we could sell
this for $28 instead of 30 and make it
just a little bit smaller, then we will
net out ahead. We'll make an extra
dollar per unit and our conversion rate
might even be higher because it's a

## Chunk 50
cheaper product. Okay, I almost forgot
that we downloaded all of the Alibaba
scrape results. We'll see how those
differ to the image search results.
We're going to take that. We're going to
start in our Google sheet. And I love
how it has a column forQ, minimum order
quantity, it says the name of the
supplier, how many years in business,
the URL to the product here, and then we

## Chunk 51
can just do this. We can just filter and
sort by price. And let's make this look
a little cleaner. So, which one has a
low price and a low minimum order
quantity? Just so happens that the one
we just looked at anecdotally is the
number one. It has the cheapest price
and ah 100 minimum order quantity, but
with a cheap price, it's fine. And you
know what? It's a brand new supplier.

## Chunk 52
So, you could look at that negatively
saying like, ah, I don't know, are they
reputable? They might not be. Or you
could look that at that positively and
say, "These guys are really hungry to
make a name for themselves or they're
willing to sell at a very small profit
margin or even at a loss so they can get
their first customers." We won't really
know which is true until we test. Okay,

## Chunk 53
let's do two more categories and I want
to give you four more strategies on how
to look at this to best ensure that you
make a lot of money in doing this. Okay,
now what's a category that is not going
to go out of style? anytime soon. Health
and wellness. Coincidentally, when Jeff
Bezos launched Amazon, he said to
himself, "What are people never going to
stop wanting? They're never going to

## Chunk 54
stop wanting fast delivery. We're only
going to want faster and faster delivery
forever. We're only going to want
cheaper and cheaper prices forever.
We're only going to want higher and
higher quality forever, right? So, I
don't see a future where humans want to
be less healthy. I think that's a trend
that's only going to keep growing. So,
we'll go health and wellness next. We'll

## Chunk 55
find a winning product and then we'll
round this out with my favorite
category, books and education. Very
unsexy, very boring, very, very
profitable. Okay, so we're going to go
back to these ID codes, foam rollers,
massage guns, sports recovery products,
health and household. The shorter ID
numbers are the more broad categories,
and I want to go broad right here. So,

## Chunk 56
instead of going like very niche on foam
rollers, I just want to see health and
household. So, we're going to copy this.
We're going to go back to Oxyabs. Hit
the drop down. Amazon. We're going to go
boom. Best sellers. We're going to paste
that browse node ID. Parsing is true.
You probably remember all this already.
Amazon domain is.com. Location. We'll do
the same zip code that we did before.

## Chunk 57
Local, United States, English in my
case. Boom. Submit request. Boom. There
we go. Took about 30 seconds. We're
going to click export. You know the
drill. We're going to convert the JSON
to CSV. Okay, there it is. We got a new
tab here called Health Amazon. Paste
that in. We got clickable URLs. And you
already know what we're going to do.
Okay, first of all, lots more ratings in

## Chunk 58
the health and wellness category. That's
a good sign. Hundreds of thousands. Holy
crap. Paper towels, toilet paper, makes
sense. Batteries. Yep, yep, yep, yep,
yep. All right. Now, before you think,
"Ah, this is too crowded. Oh, this is
too competitive. How am I going to
compete with Bounty and Scott and Amazon
Basics? Don't worry about it. Don't
worry about it. Just because something

## Chunk 59
seems saturated doesn't mean it's
saturated. It just means that it's a
popular category. It really has no
correlation on if there's more demand
than supply in that category or not.
We're going to have to learn that for
ourselves with this hard data. So, which
one in the top 50 has the lowest ratings
count? Okay, these paper towels right
here. That's interesting. We're going to

## Chunk 60
do conditional formatting. Boom. Boom.
Lower is better in this case. Paper
plates. Electrolytes. Okay. Element
electrolytes. Three ply paper towels.
Okay. So, I already know what you're
thinking. You're thinking, "How can I
compete with Bounty and Dude Wipes?" And
yeah, stop. We're not going to be
importing toilet paper and paper towels
from China. Obviously, that's

## Chunk 61
unrealistic. But what this is telling us
is the volume of buyers coming through
these categories is outrageous. So, we
want to find a tangential category that
we can sell to. So, what we're going to
do now, we're going to take this scrape
and scrap it. We're going to scrap the
scrape and then get another ID for a
tangential Amazon category such as paper
towel holders, bamboo kitchen

## Chunk 62
accessories because bamboo is so hot
right now. Stuff like that. Kitchen
accessories that they can use alongside
these things. So, we can still piggyback
on the amount of volume that's flowing
through Amazon on these exact products.
So, I've got the node ID for paper towel
holders. We're just going to find best
sellers of those. So, we're going to go
back to Oxyabs, paste in that node ID.

## Chunk 63
Boom. I'm going to keep everything else
the same. And then start scraping that.
Okay. Boom. There we go. 50 paper towel
holders and other kitchen accessories
sorted by bestseller rank. And then
we've highlighted the green ones to look
extra interesting here. This one is the
eighth best seller and only has 136
ratings. So, let's look at what it is.
Paper towel holder, wall mount, self-

## Chunk 64
adhesive, no drill or drilling. I wonder
if that's why. Five bucks. Holy crap.
Stainless steel for five bucks. How the
heck are they getting this? So, let's go
find out. Oh, man. So, here's what I
did. I went to Alibaba. I did the image
search just like I did before. And what
do you know? 40 cents to $1.77 for the
same item. Amazing. And I really like
this one because it's small enough that

## Chunk 65
we can get it shipped much more cheaply
without having to go through seaf
freight. I mean, that is the exact same
picture. So, you can apply the same
magic, same strategy, same math that we
did to the pet accessories here. And
it's pretty clear there's opportunity
here. I mean, if you look at this 15,000
ratings, if 2% of those people who
purchased it rated it, then that's

## Chunk 66
750,000
sales for this stupid thing right here.
Look, 8,000 people bought it in the last
month. Incredible. But the question is,
what other kinds of arbitrage
opportunities can we find in the Amazon
scraping results? Okay, so we've been
looking at the gap between the
bestseller rank and the number of
ratings, which is great, but what else

## Chunk 67
is there? Well, for one, I like to look
at the one star test. That's what I call
it. You don't just want to read the
negative reviews. You want to count the
one star/ negative reviews by review
type. What are they all complaining
about? Are they all complaining about
the same thing? In my experience, about
40% is the magic number. If 40% of
one-star reviews are mentioning the same

## Chunk 68
quality control problem, shipping
problem, coloration problem, etc., then
there's a big opportunity because you
can just take that same item, fix the
problem that everyone's complaining
about, and sell it at the same price.
And remember, if Amazon sees that your
comparable product has fewer returns
than the one you're competing against,
they will boost yours in the search

## Chunk 69
results. Another thing is the photo
matching. If you notice on this paper
towel holder, the Amazon seller used the
exact same stock photo that they got
from Alibaba. That does not signal good
branding or good quality to the
consumer. It's lazy. You want this
product to look like a whole company was
formed around it. People want to see the
product in use, not just in a stock

## Chunk 70
photo, but in a real kitchen, even if
the quality of a picture isn't as good.
And I cannot emphasize enough how
important that first image is on your
Amazon listing. That's what people's
eyes go to first. The titles are a mile
long. They're not reading all that.
They're looking at the image. So, you
cannot be too careful or too strategic
with the image that you pick. And then

## Chunk 71
don't forget the variation opportunity.
You can use Oxyabs to scrape items and
look at all the variations they offer in
color, size, bundles, etc. Then go
scrape the Q&amp;A section and the review
section and see where people are saying
words like, "I wish, I wish, I wish,
wish this came in a bigger size. I wish
this came in black or white or in a
bundle." Then go back to your

## Chunk 72
manufacturer or go back to Alibaba and
ask them to do that. Hey, can you do
this in white? Can you do this in black?
Of course they can. And again, take
close care to look at the shipping
weight and dimensions because there's
opportunity there. If you see a winning
product sold for 25 bucks and then you
look at the Amazon categories for sizes
and what thresholds they have for fees

## Chunk 73
for any given size or weight, at what
point do they get bumped to the next
highest fee tier? There's opportunity
for you to take that exact same product
changing nothing except for the size of
the product just a little bit, shrink it
down a little bit, either the weight or
the dimensions to get it in a lower fee
tier because that could be the
difference between $13 in Amazon fees

## Chunk 74
and $10 in Amazon fees. And that $3
difference will be pure profit to you. I
just can't help but screenshot these
kitchen accessories, send them over to
Claude, and ask which ones it finds to
be the most opportunistic for us. So, I
took a simple screenshot and said,
"Okay, of all these products, which ones
might be the most profitable for us to
copy and sell, and why?" All right, this

## Chunk 75
is very interesting. It likes number 28,
this countertop stand, because the 4.8
rating at 25 bucks means almost no one's
returning it. I love that. It likes this
one, but it says $8 is too cheap. That's
another thing to consider is using
Amazon ads to push some of these items.
You're going to need a little extra
margin in there to pay for those ads.
Okay, so it says to go after number 28

## Chunk 76
and 17 because 17 is heavy duty, higher
price, and more margin. Super helpful.
Now, I've got more strategies to
discuss, but first I want to scrape the
third and final category, and that is
books and education. So, we look over
here at the category codes and we're
going to go down to books and education.
Now, you'll notice that these ASIN's,
these identification numbers are very

## Chunk 77
low. That's because Amazon started only
selling books back in the '90s. So, the
business and money category of books was
the third category that Amazon ever sold
inside. But, we want to go niche here
because there's millions of books on
Amazon. We're going to go education and
teaching because that's where the real
money's at. I don't know if you saw this
video I posted back in December with

## Chunk 78
Mindy. She buys entire pallets of books
for a dollar and makes thousands of
dollars selling those same books on
Amazon and eBay used. And most of the
most profitable books are in the
education and teaching categories. So
that's where we're going to look today.
By the way, that video is linked below.
All right. So let's go copy that code.
We go back to Oxyabs. We're going to

## Chunk 79
keep it on Amazon bestsellers. Change
out the browse node ID. Keep the parsing
at true. Keep the zip code the same.
We're keeping everything else the same
except the product ID. Then we submit
the request and watch it scrape. All
right, our books are done scraping. So,
let's get these back into our Google
sheet, which remember you can have this
for free in the show notes below. Okay,

## Chunk 80
here's what we got. A lot of green here,
lot of opportunity, but that's kind of a
false flag because this first one of
89,000 at the top is really throwing off
the scale here because this range is all
the way from six reviews to 89,000. So,
that's not giving us an accurate
picture. I'm going to fudge the numbers
here and change it to be like 30,000 to
make this color shading a little more

## Chunk 81
accurate because we're not going to
choose these top two anyway. So, I'm
going to make this one 15,000 and this
one 15,000 to make these shades of green
more in line with everything else. So,
first of all, the six stands out, but
then I see the 2.3 rating. We can't
trust that rating one way or another
because it's not a big enough sample
size. Only six people have rated it. So,

## Chunk 82
we'll ignore that altogether. Now, let's
go ahead and format these as well, which
we've never done. So, we can see the
ratings that stand out the most. We're
looking for green on both of these
columns right here. So, I'm going to
drag them side by side. And okay, $4.
Don't love that. Let's also put the
price with conditional formatting so we
can easily see that as well. Okay, so

## Chunk 83
what we want to see is green on all
three of these columns as much as
possible. Two out of three ain't bad.
So, my eye keeps coming back to this one
right here. preschool paper crafts. This
one, learn to read. Now, there's another
prompt you can run with Claude. That's
super super helpful for stuff like this.
So, I'm going to say I'm going to
screenshot this. Go back to Claude. Drag

## Chunk 84
the screenshot in. And we want to learn
from these titles, right? So, I'm asking
Claude to say, "What commonalities do
you see in the titles of these
best-selling books that I can learn
from?" Okay, this is brilliant. Almost
every top performer falls under the same
structure. what it is, what it does, who
it's for. And you know what? You could
use that same structure for selling

## Chunk 85
anything. This is this is good. So,
let's say you want to sell on Etsy.
Boom. Take these same first principles
about titles and sell printables on
Etsy. They don't have to be books. They
can be printables, word searches,
posters, coloring pages, doesn't matter.
Use the same principle in those Etsy
titles. Oh, and it just so happens I did
a full tutorial on making and selling

## Chunk 86
printables on Amazon and Etsy. That
thumbnail is right here, and you can
also find that link below in the
description as well. It's saying stuff
like specific patterns, stack the
skills, lead with quantity, age gate
everything. This is good. You'd think
that like age gating in the title would
exclude people, but really what it does
is hyper narrow down the type of buyer

## Chunk 87
that you're looking for. Parents of kids
ages four to 8, 5 to 6 or whatever. Oh,
and Claude says that learn to is the
highest intent keyword prefix. Let's go
ahead and look at this one that we like
right here. Learn to write site words,
yada yada yada. We're going to open it
up. And you're probably thinking
something like, Chris, this is dumb. I
can't import kids books from China. And

## Chunk 88
I'm going to say, of course you can.
Look at this. We're going to do an image
search on Alibaba for this book. Come
over here. Boom. 85 cent books. And yes,
those things are stupid cheap to ship
because they're so small and light. 33
books for $12. Brand new. I mean, look
at this one right here. Oxford Reading
Tree. 33 books. We go to Amazon. We type
in Oxford Reading Tree. 33 books. 167

## Chunk 89
bucks on Amazon. $12 on Alibaba. Now,
keep in mind, buyer beware, okay, this
is my disclaimer. We're not trying to
violate any trademarks or copyrights.
China is not exactly known for caring
about trademarks or copyrights. So, do
your own research, be careful, be
ethical. You're probably going to be
much safer ordering generic kids books
or coloring books that don't have any

## Chunk 90
copyrights or trademarks attached to
them whatsoever. Like for instance, this
kindergarten workbook right here is only
80 cents. Go to Amazon, type in
kindergarten workbook. Look at that one.
It's the exact same $7 with 8,700
reviews. And what would you know? You go
back here to our sheet, 8,700 reviews,
kindergarten workbook. That one has two
out of three that are great, that are

## Chunk 91
green. But let's talk a few more
strategies before we close this out.
You're going to want to also look at the
rating distribution shape. And what is
that? Well, you're going to use Oxyabs
to scrape the ratings again. How many 5
4 3 2 1 ratings are there per product?
And just think of it this way. Consider
a product with 4.0 average rating. And
that could be mostly fivestar reviews

## Chunk 92
and just a couple one-star reviews,
bringing it from five to four. Or it
could be 50% fivestar and 50% threest
star reviews giving it a four average as
well. Those could be two very different
products with very different complaints
or compliments. If it's mostly five
stars and a few one stars, it's probably
a manufacturing defect, which is
somewhat fixable. But if the ratings are

## Chunk 93
more evenly distributed across 1 2 3 4
5, then that's going to be a harder
problem to solve because it could be a
fundamental problem with the product
itself and not just a feature of the
product that's defective but fixable.
And another thing to do here, one of my
favorite things to do is a seasonal
trend overlay. So one of the top books
in this scrape is around ACT test prep.

## Chunk 94
So, let's go over to Google Trends and
look at the ACT test prep over the last
5 years. Type it in. Look at that up and
to the right. Very interesting. And
that's not just something that's unique
to Amazon. And of course, we'll have to
remember there is some seasonality to
act test prep, but regardless of the
season, it's still trending up
nonetheless. And don't be afraid of the

## Chunk 95
word seasonal. You know that Christmas
tree vendor on the corner that shows up
every November? That guy prints money.
He doesn't lose any sleep because he
quote unquote only has a seasonal
business. He makes all of his money for
the year in two months. Seasonal is
great. It's easy to plan for. And
remember, another of the top options in
our sheet was trace letters. Look at

## Chunk 96
that. Over the last 5 years on Google
Trends, the phrase trace letters is up
and to the right. And that is not
seasonal. That's a title wave. And
another strategy to look for is the
Amazon choice badge. You'll see that on
listings, and it looks about like this.
So, anytime you scrape a category and
multiple products have an Amazon choice
badge, that means that Amazon can't

## Chunk 97
really make up their mind or decide who
the category leader is. So, with this
product type, that means there's still
opportunity for you to become that
category leader. And that's it. I just
showed you how to scrape and analyze
Amazon products in three different
categories: pets, household supplies,
and books. There's something for
everyone in this video. And I'm here to

## Chunk 98
tell you today that there are still
millions of dollars to be made on
but you got to be data driven. And don't
be afraid of the phrase data driven.
It's not as complicated as it sounds on
the surface. I just showed you. It's
looking at numbers. And remember, as you
watched this video, you probably thought
of a friend or a family member that
might like to sell something on Amazon.

## Chunk 99
Please share this with them. It would
mean the world to me if you did. You
would help enable entrepreneurship. And
remember, please check out Oxyabs. They
support the channel. I use them on a
regular basis. I wouldn't promote them
if I didn't love them and actually use
them. So, go to oxyabs.io/cris
and you can get up to 2,000 scraped
results for free. Remember, today we

## Chunk 100
only scraped a couple hundred. With my
code, you don't even need a credit card.
If you end up scraping more, you can use
promo code Chris for 20% off all Oxyabs
credits and all Oxyabs plans. Thanks for
hanging out in the Kerner office and we
will see you next
