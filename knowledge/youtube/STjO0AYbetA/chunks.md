# Chunks

## Chunk 01
Gemini have just released a brand new
embedding model that can take in as
input text, images, video, audio, and
documents. And not only is the
performance way better, it's actually
significantly easier. And when we
combine this with clawed code, we can
unlock incredible capabilities for your
business. So, in this video, I'm going
to show you what it is, how you set it

## Chunk 02
up, and an actual use case that you can
implement today following me in this
video that will improve what you're
currently working on. So grab that
coffee as I say right here and let's
dive straight in. So goes without saying
this is state-of-the-art and a brand new
release. It is kicking butt and is
crushing it on benchmarks. Now what kind
of new use cases have we unlocked with

## Chunk 03
this? Well, semantic search, sentiment
analysis, obviously it's rag. I'll
explain what that is in a second. And
there's lots of cool technical mumbo
jumbo that has come alongside it. But
let's talk about what we can build with
this. So we have rag and context
engineering. AIS, as I'm sure you may
know, can sometimes hallucinate. In
other words, they are confidently

## Chunk 04
incorrect. And we estimate that happens,
I think it's something like 2 to 10% of
the time. They'll just make things up.
When we use retrieval augmented
generation, which is the technique I'll
show you in this video, it just means
that it's way more accurate, which is
good for us because we can depend on it
for our customers and for our clients.
Right now, it uses some really cool uh

## Chunk 05
methodologies to achieve that. What is
really cool though is semantic search.
So it will analyze content across
different file types and find related
information regardless of the format.
That's the key difference here
regardless of the format. The multi-
modality that really is the USB of
Gemini, the Gemini ecosystem that
Google's crushing with right now. And

## Chunk 06
then we have this different
classification. So you can feed it text
and images, videos, audios. Think about
like any YouTube videos or PDFs,
anything you've got in your business.
How freaking cool is that? It's really,
really decent. Now let's come over and
think about the different modalities. We
have text, we have images, we have
video, we have audio and documents and

## Chunk 07
PDF for example were always typically a
a difficult thing. That's now become way
easier. And if you were to go back in
time only say 6 months ago or even a
year ago. So I flocked to New York last
year to compete in a rag competition,
the first of its kind, a gentic in the
world. And I spent like a week going
very very deep in rag and I can tell you
the kind of ingestion pipelines, the

## Chunk 08
complicated workflows. We need this for
PDF, but if it's a PDF, we've got to do
this was wild. Now we can do this in an
unbelievably easy way when we bring in
cloud code. And I'm going to show you
how you do that very, very shortly. So
all that to say, big news, very very
helpful. Now, it's got some different
interesting um technicalities to it
which you can dive deep into and I'll

## Chunk 09
put a link for you down below which is
really interesting, but I just want to
touch on what rag is. So, if you think
about the way that most people use a
chatbot is every time the context is
loaded back into the conversation. What
rag retrieval augmented generation is is
imagine you and I are in a library
together. Okay? And in this library
there's a librarian and we handle 100

## Chunk 10
books. all the Harry Potter books, all
the Game of Thrones books, all the Lord
of the Rings books, right? And what
we're saying is instead of giving all
that context to a model in every
conversation, it would a burn through
all its context window and it will just
hallucinate. What the librarian does is
say, "Thank you, Jack." And she'll chop
all those books up into a million

## Chunk 11
different pieces and she'll store them
in a huge giant mystical bookcase. And
what rag enables us to do is instead of
grabbing all 100 bucks at the same time,
we'll ask it a question like, you know,
what was the cloak of invisibility like
who who first wielded that? And what it
will do is convert that question into
learn numbers and then find the best
bookshelf to go and grab that from. And

## Chunk 12
so we'll only grab that one specific
chapter or one specific section that we
need. And where Gemini takes this to a
new level is it isn't just text anymore.
It's videos, it's images, it's audio,
which makes the whole process way
easier, which means that you and I can
have confidence in our business and
we're talking to our clients or our
personal projects that not only is it

## Chunk 13
accurate, but we're not going to have
those hallucinations. So, this is really
cool and the coolest thing is that it's
easier than ever to set up now with code
and we're going to do that inside
anti-gravity. And so, first place is to
come to this link here to get the API
documentation for this new Gemini model.
And what we're going to build together
is a chatbot. We're gonna build

## Chunk 14
something for let's call it Alex Horozi,
right? Which is if I come on YouTube
chat, I have this Horoszi bot. Now
Hormosbot is trained on all of Alex's
PDFs and all of his information. So you
can ask a question like, hey, what are
the four ways to grow a business and
it'll go ahead and it will tell you that
I want to recreate this with Alex's
books. I'm using Alex's books because

## Chunk 15
it's number one in, you know, for
business. So if you wanted to chat to
your own horos, how would we do that?
Well, we can do this now with a new
embeddings, right? It's got all the
different stuff. So how would we do
that? So the first thing we do is come
to embeddings documentation. We're going
to copy all of this. Then we're going to
head over to anti-gravity. Create a

## Chunk 16
brand new project with an anti-gravity
at the top by clicking file uh open
folder and then creating a new folder.
And then what I'd love you to do here is
just install claw code on the left hand
side by coming over to I believe it's
extensions on the left hand side. Click
on that and then you install it. Now
once you do that you'll be prompted to
connect to color code which you can do

## Chunk 17
via your typical subscription. So if
you're paying $20 a month to CL code,
you can use that within the terminal
here, which is fantastic. So what we're
going to do then is double click. And
when we double click, Claude appears.
And we click on Claude here. And we can
ask it questions. Now, we're just going
to give it a prompt. So we're going to
say, "Hey, what I would like to do is

## Chunk 18
use the brand new Gemini modalities for
ingestion. And what I want to do is
create a chatbot. But I first of all, I
want you to connect to Pineco. And I'm
going to give you three PDFs. And what I
want you to do as free PDFs is ingest
them using this brand new model. And
then once we've done that and we're
happy that's all been done, we're going
to create a chatbot online using uh

## Chunk 19
Claude and then we're going to able to
ask it questions. So below is the
documentation. The first thing I'd like
you to do is actually just install any
dependencies. First thing you want to do
is connect them to um the wonderful
Gemini. So we're going to paste all this
information here. And the model that
we're going to use to connect it to is
Pine Code. Now, I have so many people

## Chunk 20
using this uh and this is all run on
Pine Cone. Pine cone I like because it's
got a very generous free tier. And like
I said to you before, the reason why the
model's so important is because it's
realistically the librarian. You can
have a level one librarian, doesn't
speak any English, and doesn't know
where where they are half the time, or
we can have a level 10 librarian. And I

## Chunk 21
found in all the testing I did that the
librarian is really the driver of the
quality, which is so so important. So
this is now asking us lots of
permissions. So we're going to go ahead
and do this. And the cool thing about
Claude Code now is the fact that it
really will walk you through. I think
that what will separate the beginners
from the pros is your ability to

## Chunk 22
articulate what it is that you want and
understanding of structure which is a
lot of stuff that we channel. So all
dependencies are successfully um
installed. So next you want to do now is
store them in Pine Cone. Awesome. So
what we need is go ahead and grab our
Pine Cone API key. To do that, just
simply come over to Pine Con like so.
You can create a brand new environment.

## Chunk 23
You don't even need to create an index.
You just create an account for free.
From the left hand side, come over to
API keys and then click on create a
brand new API key and click on this
plus. And we'll call this one Gemini.
And then you get an API key generated.
Copy that and then head straight back
over then to Claude. And then we're
going to share the API key with Claude

## Chunk 24
and confirm that it's connected. So I'm
going to say, "Hey there dude, here's my
API key to Pine Cone. Please confirm
that it's connected and that you are
ready to ingest the PDFs. Wonderful. So,
so look at this guys. Pine cone is
connected and working. You have no
existing indexes. We'll create one for
as we ingest. I'm ready to go. So, what
it wants us now is a three three PDFs

## Chunk 25
and a Gemini API key. Cool. So, what
we're going to do first of all is drop
in the PDFs that we've got here. So, if
I click on Homozy PDF, for example, you
can see we've got these three here. So,
let me put these into a folder and I'll
call them Homozi
PDF with a load of S's. And let's just
grab these ones and then drop it in. So
these are from home books, right? We

## Chunk 26
bring that one over, drop it in, and add
folder to workspace, which now means we
now have all of these PDFs, which is
really cool. So this has got images,
it's got everything. So I'm going to ask
it now to ingest all this stuff. But the
first thing we need to do is go ahead
and grab our Gemini API key. And we can
grab an API key by coming to a
studio.google.com/apien

## Chunk 27
keys, create a brand new one, and then
just copy that API key, and then provide
that over to Claude with an
anti-gravity. And just like that, it's
now confirming the Gemini embedding 2
preview is connected and also pine
curve. So send me your three PDFs and
we're ready to go. To remove the
anti-gravity panel, by the way, it's
just command and L. We're not I think

## Chunk 28
come here and does it. Yeah, it's okay.
Cool. Sounds awesome. Go ahead and do
it. I put it all under the homozy PDFs
on the left hand side of this project. I
would like you to basically ingest them
all into a pine cone index and create
that for yourself, please. So we've told
it to go ahead create the index and
ingest the information. Beautiful. And
of course, for speed of text, we're

## Chunk 29
using glider. Some say the world's
fastest speech to text. I'll let you be
the judge. You can test it out for
yourself. Now, the cool thing here is
that we can pretty much just give this
all the information that you actually
want. We could, if we wish, ask it to go
ahead and scrape. So, the one that I've
got set up in AI with Jack is I actually
have it scrape all of the videos. So, it

## Chunk 30
takes all of the transcripts every
single time and adds it. And we set this
up to run on a regular basis. So, every
day it will check for new videos. If
there's a new video, we grab it, we pub
text, and we bring it in. Now, one
little hack that I want to give you here
as well. And in fact, let me just give
this a bit of an additional pushin. Hey,
dude. One of the things that you'll

## Chunk 31
notice is that within the books, there
are graphics, there are images. I also
want to be able to retrieve those
images, retrieve those drawings, those
scribblings when I ask it questions. So,
that's really important that I'm able to
do that. Okay, awesome. Just to be super
clear with my stated intention. Now
little hack for you on rag that you
think we might find really helpful while

## Chunk 32
this is working in the background here
is that typically speaking we also want
to apply a waiting index. So I created
ask me questions, right? So you can
literally come over to me and say, "Hey,
how do I get my first client? What is
anti-gravity?" Whatever. Now, one of the
things that you find very quickly when
you build a chatbot using rag, which is
probably one of the predefining

## Chunk 33
features, is that it treats all
information equally. It's very very
generous, very very PC with that. But in
reality, there are certain occasions
where we don't want to treat all
information equally. Right? So it's it's
pulled up classroom lessons now. So I
can click this. Let's have a look. Now
I'm in my classroom. So cuz this is
traditionally issue with certain

## Chunk 34
platforms is has a plethora of gems. But
how do we surface the gem book to make
it easy to access? So one of the things
you quickly find with this is that it
treats all the information equally. So
what you typically want to do if it's a
chatbot like that is we can apply a
waiting. So the waiting that I find
works like a charm for me is we say
anything within the last 3 months gets

## Chunk 35
almost like an additional boost. So it
doesn't disregard older stuff, but
especially in an industry like AI where
everything's changing, some advice from
a year ago isn't as relevant as it is
today in 2026. So I apply a kind of
waiting. So like if it happened in the
last 3 months where we're talking about
things like anti-gravity, Google's
anti-gravity and cloud code that gets

## Chunk 36
bumped up way more than maybe some
make.com uh thing from two years ago,
right? Because you wouldn't want to
surface that. So that's really
important. If however you're looking at
something like you're working with a
medical practice or you're working with
a legal firm that's a slightly different
kind of rag. Now there's two types of
rag you really want to understand.

## Chunk 37
There's what we call global rag and
there is local rag. Global rag is
imagine our librarian for example and we
say to her look I want to know about
Harry Potter's invisibility club. What
global rag is is she will reach over or
he will reach over grab the book and let
you know about it. But it will also
bring in and introduce information and
context from other books in its

## Chunk 38
knowledge. So it will know that the book
talks about the invisibility cloak, but
it might also know that well actually
there's other thing I know about Harry
Potter law that's not inside the books
and it will it will kind of sprinkle all
of this knowledge in. We call that
global rag. Then we have what's called
local rag. Now local rag is very
specific. It's something like if you

## Chunk 39
were consulting an insurance document,
okay? And I only could only possibly
want what's in the information, right?
Think about notebook LM works in this
manner. It really is strict on the
resources you give it. If you put
garbage in, you get garbage out. So that
would be useful if it was something
like, you know, let's think about an
insurance agency and you wanted to ask

## Chunk 40
questions about HR policy or would they
be approved. It will only bring back in
local rag that specific information. So
you can see that getting the injection
is one thing but as always the devil
lives within the details and wonderful
just like that it's begun to index it
which is fantastic and we can actually
prove this guys by coming over and you
can see now the homoy box has been

## Chunk 41
created. So if I click on this let's
have a look at what we're dealing with
and as you can see it's got all these
different results. So if I hover over
this you can see it's got everything
there which is really cool. So next step
is to turn this into a chatbot that we
can have a conversation with. So let's
come back over to anti-gravity. I'm
going to say awesome. What I'd like you

## Chunk 42
to do now for me is create for me a
chatbot in a local host that I can then
use and I want you to use the let's just
say opus 4.6 sonnet and I would then
like to use the below API key to do this
please. Cool. And then what we want to
do guys is head over to open router. So
open router basically just lets you chat
with any model and I love it because we
can use opus 4.6 six is Albert Einstein

## Chunk 43
the genius and then for less tasks you
know we wouldn't want Albert Einstein
mopping our floors right we'd want him
in the library working hard on our
wonderful embedding models so what we
can do is on open router create an
account you can then come down on API
keys on the left hand side come over
then create a brand new one you'll get
an API key just bring that back over to

## Chunk 44
claude and then ask it to complete its
job and the other thing that I did guys
is I took a screenshot of this cuz I
want the design to look amazing I came
back over and I said hey to anti-gravity
improve it Now bear in mind this is one
shot and the first thing that it came
back and gave me here looked like this.
Some saying that amazing and then when I
gave it the prompt it then came back

## Chunk 45
with something like this. Again we can
improve it but the point is we want to
see that this rag actually goes ahead
and works. So let's go ahead and give it
a test. So I'm going to say hey there
dude what is the value equation? Bam.
I'm going to see what it does when it
comes back with. Now bear in mind I've
not come back. I'm amazed that it knows
exactly how to show that graphic as well

## Chunk 46
but bear in mind I've not actually given
it any prompting or specifics on the
information I get it back. And always
remember with rag, you need to always
fine-tune it for your specific use
cases. Okay, so we're going to see now
ask a question and see what it comes
back with. Okay, and just like that,
we've got some information here. So
we've got quite a lot there. The value

## Chunk 47
equation is the framework Alexi created
to quantify blah blah blah, the four
drivers. We've got the information, the
competitive edge, and at the bottom,
it's actually grabbed us these
screenshots from the book. Really
freaking cool. So, what we'd need to do
is come back over to anti-gravity and
say, "Hey, I want you to keep the
responses concise. Literally, no more

## Chunk 48
text than needs to be." So, typically
speaking, there should be no more than
five lines maximum. And when you're
bringing back images and graphics, let's
actually not bring back any more than is
relevant. So, it needs to be great for
the user experience. Don't just show me
everything. Keep it crisp. So, we need
to we then flirt with I say flirt, but
we dance with the model. Explain some

## Chunk 49
specifics. Okay. But then I open a new
tab, guys, and ask it the same question.
Show me the grand slam offer diagram.
says, "Give me some information about
what it is." Let's see if I can find it.
And look at this. It's pulled it up.
There's the Grand Slam offer diagram.
So, you can see the multimodality of
this. It's pulling back images. It's
pulling back text, which is literally

## Chunk 50
incredible. And so, now we understand
exactly how to build this beautiful rack
system. The next thing that we need to
do is learn how to make it look gorgeous
and host it online so we can share it
with our customers, which we can do by
watching this video right
