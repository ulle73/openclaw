# Clean Transcript

OpenClaw just dropped version the 11th
of March and this update is packed with
some awesome stuff including new free
models with 1 million context windows
that just showed up on open router. That
means you can feed an entire book into
an open core conversation and get
answers back completely for free. Gem's
new embedding model just got wired into
OpenClaw's memory system, which means
your AI agents can now remember images
and audio, not just text. And there's a
whole new onboarding system for running
local AI models with Olama. So, even if
you've never touched a terminal in your
life, you can set this up. And this is a
super easy update that I'm going to run
through today. And I'm going to break
down the whole thing, show you what
changed, show you what you can build
with it, and give you a step-by-step
framework to go from, "I've heard of
Open Claw" to I have agents running my
business. I'm also going to give you
every single prompt you need, copy and
paste, you can follow along. And if
you've been sitting on the sidelines
thinking OpenClaw is too complicated or
too expensive, this update literally
removes both of these excuses. So, you
can see the details right here. Hunter
and Healer Alpha have been added to
OpenClaw. Now I've already got this
running inside my open claw right here.
So we're running open router with hunter
alpha and you can see the update is now
available. So we can just click update
and run to the next version. Now here's
the full change log of everything that's
changed um what it means etc. And I'll
run you through it right now. Okay. So
this update is pretty big. You can see
it's a it's a big change log file with a
lot of stuff going on right here. And
the thing to note here is that this
includes security fixes, new features,
and changes that affect how your AI
agent runs every single day. Now, before
we get into this, you might be thinking,
okay, what even is OpenClaw? So, I'll
make this brief in case you've never
heard of it before. Think of OpenClaw
like a super smart AI assistant hub. It
connects to AI models like Claude, GPT,
Gemini, more. It lets those AIs talk to
each other, run tasks automatically, and
and Slack. And it runs on your Mac,
iPhone, or a cloud server. So, think of
it like a brain that controls all your
AI bots and your robots. Um, and this
just this update just made that brain
smarter, faster, and safer. All right.
So, it's basically the operating system
for AI agents. So, let's talk about what
happened and what's changed. So, one of
the biggest updates that we've seen so
far
is
that we have now got a new security
update which you can see right here.
Now, what does this mean? Well,
basically there was a security hole in
openclaw's websocket system and a
websocket is just how your browser talks
to the openclaw server in real time.
Problem is bad actors could sneak in
through the wrong door um and get admin
access your open claw gateway. This
means they could control your agents,
read your conversations. What's fixed?
Overclock now checks where every browser
connection is coming from before letting
it. So, it doesn't matter um how they're
trying to get in. Basically, it's much
harder to break into. On top of that, uh
iOS just got a huge makeover. So, it has
a new home screen. Open floor on iPhone
just got a brand new welcome screen.
When you open the app, you'll see a live
preview and overview of all your running
agents running in real time. You can see
the full details on this. the home
canvas like so and it refreshes
automatically when you reconnect or come
um back from the background. Cleaner
controls. So the old floating buttons in
the corner are gone. They been replaced
with a clean dot toolbar at the bottom.
Right. And also we've got smarter chat
tools so you can pick your AI model
right in the chat. Now there's now a
model picker right inside the chat
window on Mac. So you can switch between
claw, GPT, Gemini and more without going
into settings and thinking level stays
safe. So if you told open claw before
how deeply you want it to think about
problems, that setting now stays saved
even after you restart your Mac or
whatever. All right. So you can see here
um and I just want to show you this
because like if you have the same issues
then you know how to handle this. So you
can see here that it has stopped
running, right? So when we clicked
update it's totally broken. Um, so what
we're going to do is try and restart the
open claw inside terminal. I'll just do
that in a second, but I think it's good
for you to see this so you know, okay,
what to do if something breaks or how to
handle it, etc. So, what we're going to
do is run this gateway again and test
out. So, go to the terminal
and try this out. Now, it's beginning to
restart. And it's back on with version
11 of March, right? And it says the
health is okay. Plus, we can reply
inside the chat. So if you find the same
problem, if your open claw stops
responding or it says health not okay in
the top right etc. just run the command
which you can see right here. So open
claw gateway and then the port inside
terminal. So you can just copy and paste
that command if it struggles to update.
Bear in mind we just use a button to
update but it's still disconnected. It
still stopped working. It's kind of
annoying but it's all part of the game,
isn't it? You can also now switch
between the primary model, right? So you
see here that we can switch between
these models that we've got on the list.
So if we go to agents on the left, then
you can switch between agents and you
can change the primary model for each
agent. So for example, we've got current
kilo gateway. We could use open eye
codeex 5.2. We're going to use Hunter
Alpha. And by the way, if you're not
familiar with Hunter Alpha, that's
because it is a brand new stealth model
that just came out. So if we go to
models inside open router, you can see
that we have two. Now you need an open
router um API API key to connect to this
right you can see how it works step by
step right here and Hunter alpha itself
has a million token context window and
it's free to use now some people are
saying it might be GPT 5.5 other people
are saying the healer alpha might be
GPT50
nobody knows even once it's um even once
this is taken off open router usually
you don't find out who the provider was
or that sort of thing there are two new
mod models and you can use them both for
free inside open core right now and it's
pretty fast and responsive when you're
using them. So that's pretty cool too.
Now let's talk about what is first of
all. Well lets you run AR models locally
on your own computer, right? So you
don't need the internet um and there's
no API costs if you're using a local
model. Now what's changed? Well,
OpenCloud now has a built-in setup
wizard specifically for Olama. So you
can choose between local only mode where
everything runs on your machine or cloud
and local mode which is a mixture of
both. Bearing in mind that cloud has
token limits, it also suggests the best
models for your hardware automatically
using this on boarding with Olama and it
handles the cloud model setup without
making you download models you don't
need. So if you want like a free way to
run open claw locally, this is a big
update that can help you a lot. I think
a lot of people are struggling with
setting up uplama uh with open claw. We
actually did a video earlier today where
we talked about how to use Neatron 3
super from Nvidia with OpenClaw and
that's a free model that you can get via
the cloud using O Lama. And if you want
to implement that, you can just use the
O Lama setup as well. On top of that,
there's also some new memory updates,
right? So, if we have a look through the
change log here, you can see there's a
bunch of new memory updates. So, we've
got Gemini embedding preview for
example, and we have an add-on uh right
here as well. There's a lot of mentions
of memory inside the change lock. Now,
what does this mean? Well, OpenClaw
already had a memory system and it
remembers things across conversations.
So, what's new? Well, you can now opt
into image and audio memory as well.
That means OpenClaw can search through
pictures and audio files you've given
it, not just text. Now, this is using
Google's Gemini embedding model, Gemini
embedding to preview to understand
what's in those files. And that just got
released very recently indeed. So you
can also configure the dimensions aka
the detail level of how memories are
stored. And when you change that
setting, memories automatically rebuild
themselves. So there's no manual work
required. On top of that, you've also
got um a bunch of agents fixes. You've
Telegram improvements, ACP for advanced
users as well. There's some improvements
right there. And uh a bunch of other key
fixes as well like you can see, right?
And if you use chron jobs aka schedule
tasks in openclaw, this is also super
useful for you. So uh chron jobs can no
longer send notifications through
workarounds. They must now use the
proper delivery channels. So you can run
this command to fix anything related to
that. Now we actually have a full
framework based on this new update like
you can see inside the video notes from
today along with
a 30-day plan on how to implement this.
But just to recap on the updates that
came out. So you got Hunter alpha and
healer alpha which are free models on
open router. You've got Gemini embedding
to preview for memory search across um
audio and images. You've got open code
go support, iOS home canvas overhaul, so
improvements on the UI of the canvas
app. Oama on boarding, better security,
and a ton of bug fixes as well. Right
now we've got a 30-day plan right here
for implementing this stuff, including
setting up O Lama. So, if you want to
learn how to use this new update to run
with Olama and really take advantage of
it, then you can check out the 30-day
plan right here. We also have a list of
100 copy and paste prompts for OpenClaw
based on the 11th of March setup, right?
So, you can see the setup and
configuration prompts right here, a
bunch of agent creation prompts, and
everything you need to really win with
this new update. But that's basically
it. And you know exactly how to update
it. You know exactly how to fix it if it
breaks like you saw today. and you know
exactly what this update is about and
how it changes things. So if you want to
get all the video notes from today, you
focused on helping you save time, scale,
and grow with AI automation. So if you
want to learn this stuff, you can get a
boardroom. And additionally, you can see
here that we have 2,600 members, which
means 24 hours a day, there's always
people online happy to help you, right?
So for example, you can see that we have
a daily accountability group where you
can post your goals and stay laser
focused. I also do a weekly update post
as you can see right here that basically
walks you through what are the most
important updates, what can you ignore
and how can you implement this stuff
inside your business this week.
Additionally, you can see uh we we do
things like this mega value thread where
people just post their best tips and you
can ask questions and get help and
that, you can get weekly video coaching
calls. You can jump on live AI
automation coaching calls like you can
see right here. You can meet people in
your local area via the map. So you can
zoom in and DM people and ask to jump on
a Zoom meeting or meet them in real
life, etc. And then additionally, you
get access to all of my best training.
So for example, if you want to get a
full six-hour course on how to set up
Open Claw and make the most of it, you
can check that right here. If you want
to get another course, we've got a
step-by-step guide and video tutorial
there. And we add new elite updates
including for example a guide on using
Hunter and Hila alpha along with Neatron
3 super with openclaw as well. And
yesterday we covered for example
openclaw paperclip which is an awesome
update for really managing like a full
structure of teams of agents. So every
single day I just look at what's coming
out, what's useful and then I create a
video tutorial and a step-by-step guide
to help you out with that. Right? You
boardroom along with a course that shows
you how to go from beginner to expert
with AI automation. You'll get access to
personally use. So, for example, how I
Instagram AI avatar videos, etc. And
additionally, you can learn how to get
more clients with the agency course. You
can watch back the coaching calls right
here if you miss them live. You can
learn how to rank number one with AI
SEO. So, we have a full system and setup
guide here. And then additionally,
you can see that we have a full
step-by-step road map on how to grow a
YouTube channel based on what's working
for me. So that's all inside the AR
comments description or just go to the
aiprofitboardroom.com.
