# Transcript

- URL: https://www.youtube.com/watch?v=5dy2ahf_EKQ
- VideoId: 5dy2ahf_EKQ
- Title: New FREE OpenClaw Update: GPT 5.4 + Gemini 3.1 Flash-Lite

## Transcript
Today we have a brand new update from
Open Claw. It's a new free update. If
you've been sleeping on OpenClaw, wake
up. This new release just dropped in
this pack with features. We're talking
about GPT 5.4 support. Gemini 3.1 Flash
Light, Slim Docker builds, and way more.
Let me break it all down for you so you
can see what is actually inside the
update and so you can actually use this
stuff. Even if you've never heard of
OpenClaw, let's get straight into it. If
you're not sure what OpenClaw is, by the
way, it's a free open- source AI agent
platform. It's like a brain. You can
connect to almost any app. You can set
it up on Telegram, Discord, Slack, etc.
Searches web, run code, uh, manages
files, uses tools, even spawns sub
agents and tasks. It's like having your
own personal AI system that lives inside
all of your messaging apps at once. Now,
why would you care about this update?
Well, there's a bunch of new features
and headlines. So, you can see GPT 5.4
and Gemini 3.1 flash light integration.
So, basically, you can use the newest
updates of GPT and Gemini. You also got
ACP bindings, uh, Slim Docker, Secret
Ref, Pluggable Context Engines, HIF
image support, and Zalo channel fixes as
well. So, we're going to get straight
into this. You can see the full change
log right here, and there's a ton of new
updates. It's absolutely packed with
features. If you're wondering what it
means, etc., um, what all this means for
you and how you can actually use it,
I'll talk you through each one in a
second. If you're not sure how to
update, literally all you do is you just
go into the chat of open claw and you
just say update for me, right? Um and
then you're good to go. And you can see
for example here we got updated to the
um 7th of March version and I asked what
API using and it's now running on GPT
5.4 codeex ath which is awesome. So it's
pretty easy to set up, pretty easy to
update, pretty easy to um use. Now let's
talk about what it means for you. So,
here's the seven biggest things you need
to use. And basically, if you're not
sure, basically, there's new updates
that come out all the time for Open
Claw, right? And often they make them
like faster or safer or more powerful.
So, the first update that you can see is
GPT 5.4 and Gemini 3.1 flash light
support. And this is a headline feature.
So, Open Claw now supports the latest AI
models out the box. GPT 5.4 is now the
default model. When you choose Open AI,
that means if you just type in like GPT
in your config, automatically uses GPT
5.4. No extra setup needed. And then
also the other one is Gemini 31 flash
light. So this is Google's super fast,
super cheap AI model. Perfect if you
want quick answers without burning
through API tokens. Open claw handles
all the weird ID model stuff behind the
scenes. You just pick your model and
you're good to go inside the onboarding.
Now the next bit is pluggable context
engines. And this one is a bit more
technical, but stay with me. I'll
explain it as simply as I can. So when
you chat with an AI, it has a memory
window, right? it can understand how
much of the conversation it can see and
when that window gets full open has to
compact aka shrink the conversation now
before the update there was only one way
to do this now you can actually build
your own context engine plugins that
means you can swap in totally different
strategies memories uh for how your AI
remembers things right it's actually a
new plug-in called lossless claw that
tries to remember and keep more of the
conversation intact right so it's better
memory across your open claw it's kind
of like upgrading your AI's brain from
like a notebook to a filing cabinet. So,
if you're just a regular user, you don't
need to do anything. Everything works
exactly the same as before unless you
install a context engine plug-in. Next
up, ACP binding. So, if you're not sure
what ACP is, basically this is a way of
like using agents inside openclaw. You
can see like the full details and
configuration how this works with um
OpenClaw normally. Now, with ACP,
basically, this stands for agent
communication protocol. It's how
OpenClaw agents talk to each other and
to specific chat channels. Now, before
this update, if you restarted OpenClaw,
your Discord channel and Telegram topic
bindings would disappear. That mean your
agents would forget which channels they
are supposed to be in. Now, those
bindings, they're saved permanently. So,
if you restart the server, your agents
pick up right where they left off. This
also works with Telegram forum topics,
and you can even bind a specific agent
to a specific Telegram topic thread. And
there are now approval buttons in
Telegram so you can approve agent
actions right before your chat as well.
Next up we have slim Docker multi-stage
rebuild. Now if you're not sure what
docker is basically it's a way of
setting up a container for your open
right you can get it for free. It's just
kind of like a safer way to host stuff.
You can actually switch things on and
off as well. So if you set up openclaw
then you want to switch it off you can
press stop inside docker and then you
can add it back in later. That's how it
works. And so with the slim do docker
multi-stage rebuilds um if you run open
core and docker which is one of the
easiest way to get it up on server the
docker image is now built in multi-stage
format that's a fancy way of saying the
final image is way smaller all the build
tools source code and extra stuff gets
thrown away your keyboard you actually
need to run open core and there's even a
new slim option you can use you can use
a variant it's called openclaw equals
slim when you build and you also get
another feature called openclaw
extensions This lets you pre-install
your favorite plugins right into the
Docker image. So when your container
starts up, everything is already there.
Basically faster start up, more
reliable, and less headaches. There's
some security upgrades as well. So
before people would put like passwords
and tokens and stuff directly into the
config file, which isn't ideal. Now
there's something supported called
secret ref, right? So instead of putting
your password inside the config, you put
a reference to where the secret lives
and it's like pointing to an environment
variable or a secret manager. This means
um your your passwords are not sitting
in a plain text file which is more
secure of course. We have H EIC image
support as well. So basically if you if
you take photos with your iPhone unless
you change your settings they're
typically going to be in a format called
HIC right and most AI platforms can't
read them. OpenClaw now automatically
converts HIC images to JPEG before
sending them to your AI model. If
someone sends you an iPhone photo in
Telegram or WhatsApp and it's HIC
format, Open Core will just handle it
which means you don't get like any
unsupported format errors as well. And
then there's a ton of like channel fixes
across the board. So there's literally
hundreds of fixes for every chat
platform OpenCore supports some
highlights. So for example, you got
Telegram. So streaming messages no
longer show duplicate bubbles. Draft
previews work properly in our DMs. Polls
are supported as native action. Native
commands work correctly. Media uploads.
So you can see a bunch of updates inside
Discord as well, Slack, WhatsApp, Lime,
FCU. Facu is a Chinese messenger app.
You got Signal as well and you got uh
Matimos as well. And then there's a
bunch of security updates. You're going
to see this is a common theme across all
the updates that come across inside
OpenClaw. So if we scroll down, we can
actually just control and F this. And
you can see a bunch of fixes um for
security right here, which is obviously
like a big concern with open call being
an open- source um example. And then
there's a bunch of uh memory and
compaction improvements. Some memory
search with QMD, the inbuilt uh
knowledge base got several fixes. So
keyword search rankings now work
correctly. Collection conflicts are
handled automatically. Duplicate content
errors trigger an automatic rebuild and
retry. This is some technical stuff. Um,
but basically what this means is that
you can now choose which sections of
your AI agent instructions get
reinjected after compaction. And this
gives you way more control over what
your AI remembers. And then there's
something called internationalization.
Right? So the web control um panel now
supports Spanish as a language. And it
includes local detection, lazy loading,
and language picker labels. And I think
there's a bunch more languages coming
soon. I've been seeing them inside every
single update adding new updates, um,
adding new languages, etc. So just a
recap on the whole update. Quick recap
in 30 seconds. GPT 5.4 is now the
default OpenAI model. Gemini 3.1 Flash
Light is fully supported from Google.
There's pluggable context engines that
let plugins control how AI manages
memory. ACP bindings persist through
restarts. Slim Docker builds secret ref
for storing passwords. HIC images auto
convert. Hundreds of channel fixes.
Major security hardening. Memory
compaction smarter and more reliable
Spanish language support. Um, and that's
basically how it works. All right. So,
if you want to get started, literally
all you do is you just go inside the
chat and you say update to this.
Sometimes you have to, for example, um,
restart the gateway, but typically it's
it's fine. And that's the whole update
right there. So, thanks so much for
watching. If you want to get all the
video notes from today and you want to
get a six-hour course on Open Claw, plus
another three-hour course right here and
daily updates on the new latest updates.
So, for example, recently we compared
Kilo Claw versus Open Claw. We also
looked at claude code skills which is a
way of kind of making um claw code up to
the same standard as open core. We also
looked recently at some of the best free
open core alternatives including 30
different versions. So if you want to
get all of this and daily updates like
you see you can get that inside my AI
automation community the AI profit
boardroom. This is a community focused
on helping you save time grow and learn
with AI. Right? There's 2,600 members
inside here which means you can ask
questions, you can get help, you can get
support whenever you need to. You can
also, for example, join our daily
accountability group so you can post
your goals and stay laser focused. We do
a weekly AI update. So, we cut through
all the noise and we just give you a
filter on my 60 hours of research. And
basically, I look at everything I've
researched, all the stuff I've tested. I
go live for about um 90 minutes a day as
well. And I just compact all of that
information into a weekly AI update
inside the AI profit boardroom so that
you can save time and also you can see
what other people working on as well,
which is pretty awesome as well. Inside
the calendar, you can get weekly video
coaching calls. You can get help and
support whenever you want. Inside the
map, you can meet people in your local
area and connect with them, which is
pretty awesome as well. And then inside
the classroom here, you can see, for
example, our best training. So, you can
go from beginner to expert with AI
automation and learn how to build your
first AI agent in under 5 minutes. You
can also, for example, get my best
playbooks on how I automate X,
newsletters, shorts, Instagram, um, AI
avatar videos as well. And then if you
want to get the daily new updates, the
new upgrades, you want to find out
what's working right now, etc., where we
do daily video tutorials with
step-by-step guides inside um this
section right here. Every single day, we
add multiple guides like you can see
each day based on what's working, what's
new, etc. Then, additionally, you can
see how to get more agency clients with
the agency course. You can watch the
coaching calls back if you don't make
them live. You can learn how to rank
number one with AICO over here. And you
can also learn how to grow a YouTube
channel with AI based on what's working
for me. So you can learn all of that
inside the AI profit boardroom link in
the comments description or go to the
aiprofitborder.com.
