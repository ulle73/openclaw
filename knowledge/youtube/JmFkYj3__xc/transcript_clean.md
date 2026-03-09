# Clean Transcript

OpenClaw just released a brand new free
update. I'm going to be talking it
through today, showing you how it works,
etc. And if you're running AI agents,
you need to know what's changed. Here's
everything new in OpenClaw the 8th of
March 2026 update broken down. So simple
anyone could follow along. So these are
the headlines. So ACP provenence, your
agent family knows who's talking to it.
Open claw backup because everyone needs
a safety net. We got Telegram dupes
removed and then 12 security fixes. You
can see the change log here. It's not as
packed as yesterday's one to be fair,
but we'll be talking through what it
means, how it works, etc. And you know,
I've got OpenClaw ready and waiting to
go with GP 5.4 plugged in over here. So,
we're going to be testing it out. Let's
just test updating it. See if it breaks
or not. We'll say update to the new
version. Sometimes it works, sometimes
it doesn't. sometimes totally just goes
offline once you've upgraded. So, we'll
see how that works in a second. In the
meantime, let me talk you through it.
So, what are some pe you know some
people say, what is OpenClaw? OpenClaw
is a free open-source AI agent platform.
Think of it like a brain you install on
your computer that can do things for
you. So, it connects to apps like
can browse the web, run tasks on a
schedule, talk to people on your behalf.
It's like hiring a virtual assistant
except it's free and it runs 24/7 and
over 43 contributors helped build this
update. Now, we're going to be breaking
down the four biggest updates. You can
see this still taking a little while to
update here. So, in the meantime, I'll
talk you through what these updates
mean, um, how they work, etc. So, first
of all, ACP Provenence, your agent
finally knows who's talking to it. This
is a big deal. Before this update, when
one agent talked to another AI agent,
there was no call ID. Your agent had no
idea who sent the message or where it
came from. Now, there's something called
ACP provenence. And this is something
I've seen as a recurring theme across
all the latest updates from Open Core.
They're always focusing on ACP and
improving it. ACP stands for agent
communication protocol. It's how AI
agents talk to each other. Provenence
means where something came from. So now
every message that arrives to your AI
agent comes with a digital receipt. And
that receipt includes a session trace
ID, basically a tracking number. You can
turn it on, you can turn it off, or you
can set it to show full receipts. And a
command um for setting it off looks like
this if you want to switch this off. Off
means no tracking, which is your
behavior. Meta um is your agent who sees
who sends the message and meta plus
receipt equals your agent sees who sent
it and gets a visible receipt injected
into the conversation. So you can sort
of switch it around using that. So you
can select provenence, meta, or meta and
receipt. And if you're building where
multiple AI agents talk to each other,
this is maybe the single most important
feature inside this release because you
now have an audit trail. You can
actually see that open claw is still
thinking about updating right now. So
it's giving me the three dots, the
classic. Um I'm sure it will fix in a
second, but in the meantime, I'll keep
talking you through what the next part
means as well. So next up, we have
openclaw backup. And basically what this
means is this could literally save your
entire setup one day. Before this
update, there was no builtin way to back
up your openclaw configuration. What
does that mean? Well, something broke,
you were starting from scratch, from
zero. Now there are two commands that
you can use. Openclaw backup create,
which means you can make a backup of
your entire setup. Super useful, right?
And then openclaw backup verify, which
checks your old backup is actually valid
and not corrupted. So, if you for
example have to uninstall and then
reinstall again, no problem as long as
you're using the backup feature, and
that's what this update is all about.
You can also use flags to customize what
gets backed up. So, if you do this, for
example, only config, you just save your
settings, not your entire workspace. If
you type in no include workspace, well,
it skips the big workspace files and
just grabs the essentials on the backup.
Every backup comes with a manifest, aka
a checklist of everything inside and
payload validation, which is a check to
make sure nothing is missing or
breaking. And here's the smartest part.
When you're about to do something that
could be destructive, like for example,
a major update reset, OpenClaw will now
nudge you to make a backup first, which
is super useful. So, think of it like
saving your game. You don't have to, but
you know you should, basically. Next up,
Telegram dupes removed. Let me just
check up on the the update again. is
still rolling out. So you can see it's
still installing. But let's talk about
Telegram backups and what they mean for
this new update as well. So if you've
been running OpenC with Telegram, you
might have noticed something annoying.
Sometimes when someone sent your agent a
DM, it would reply twice. The bug
happened cuz Telegram messages were
being tracked per session key instead of
per agent. So the same DM could trigger
two different internal routes and both
would fire off a reply. This is now
fixed. DMs are dduplicated per agent,
meaning one message in, one reply out
always. And they also fixed a second
Telegram bug where streaming replies,
where the message builds word by word,
would sometimes add a flat a duplicate
copy before collapsing back to one. Both
of those issues are gone. All right,
still not updated, but I'm keeping you
posted. And then the final part here is
the security fixes. So there's there's
over a dozen um security fixes. You can
see a bunch of them right here. And uh
this is an interesting one actually. The
skills download safety. So um the
validate tools route is now pinned
before any archive is written. Right? So
there's 12 extra features just added for
security which is pretty useful right
there. So that's basically it. And then
there's a bunch of bonus features worth
knowing. So like talk mode got a bit
smarter. U Brave web search upgrade. So
there's a new opt-in mode. This lets
your agent call Braves LLM context
endpoint, which returns pre-extracted
grounding snippets with source metadata
instead of raw search results.
Basically, it's way more useful for AI
agents that need facts, not links. You
can switch between light mode as well if
you're in the terminal. Android app got
cleaned up as well, so it self updates.
Background location, screen recording,
and background mic capture were all
removed from the Android app. basically
just to make it leaner and less
permission hungry um and probably less
buggy as well. And then Chrome restart
fix. So when openclaw restarted um it
used to replay all misch once which
would overwhelm your system. Now it
staggers to catch up so your gateway um
doesn't break. So that's basically it.
AC provenence open backup telegram
dduplication 12 security fixes talk mode
silence config brave lm context search
light terminal theme is slim down and
chrome restart staggering and 43
contributors who helped make this
happen. Nice. Now, if we go back in that
time that I've explained what the update
means, it has restarted. Um, and you can
see here it's actually downloaded the
update and then it will just restart
automatically in the background
hopefully. And you can see that it um
re-triggered a restart automatically.
So, that should come back online in a
second hopefully and then it should
upgrade to version um 8 for March. You
can see that it is completely offline
right now. Happy days. Hopefully, we get
that back in a second. And that's
basically it for the new update from
OpenClaw. How to use it, how it works,
etc. If we go back to the tab now, it
has updated. And you can see we've got 8
for March. So if you want to update,
literally just type in the chat update.
It will take about 10 to 15 minutes like
you've seen today. And then once it's
done, it's done. Happy days. So thanks
so much for watching. If you get all the
video notes from today, plus my best
trainings on Open Core. We actually
every single day to help you get the
most out of OpenCore and everything
else. Right? So, you can see, for
example, here we added a full 6-hour
course on Open Claw. We also added
another three-hour course right here.
Every single day, I'm adding new updates
on the most useful stuff inside the AI
automation industry. We also covered
recently like free Open Core
alternatives. We covered how to do AI
SEO with open. Basically, I look at
every single thing that comes out and
then every single day I create anywhere
between four to six new video tutorials,
a step-by-step guide for all the new
updates so you never fall behind again.
Also, you can see here that we actually
add um a weekly update. And what I do is
I look at all my research and then I
condense it down into what's useful,
what's not, and then uh what you can
ignore. And that basically saves you
time because I do like the 60 hours of
research per week on AI automation
tools. You see me test that stuff every
day. And then inside uh the comments you
can see like people are just uh loving
what we've said. So um people are
getting awesome results with this which
is what we like. Also in for the
have over 135 pages of testimonials
which is pretty insane. So lots of
people getting a lot of good wins out of
our school training. So if you want to
join link in the comments description or
just go to the aiprofitboarding.com
focused on helping you save time scale
and grow with AI automation. Now, we've
got 2,600 members inside, which means
that number one, you get an awesome
network of people who are doing similar
things to you. And number two, you can
share your wins, what you're working on,
etc. Number three, we have a daily
accountability group inside here, too,
so you can post your goals and stay 100%
focused. We have weekly video coaching
calls, so you can get help and support
in real time, plus ask any questions,
share your screen, and meet the
meet people in your location, so you can
meet people locally, like you can see
right here, DM them, jump on a call,
meet in real life, etc. And then inside
the classroom, you'll get access to all
of my best trainings. So, for example,
you can go from beginner to expert with
AI automation and learn how to build
your first AI agent in under 5 minutes.
You also, for example, get my best
Twitter, etc. And then if you want to
get the daily updates, the new stuff
that I'm adding every single day, you
can get it right here along with the
6-hour course on Open Core. And also, if
you scroll down, you can see how to get
more clients to the agency course. You
can uh learn how to rank number one with
AI SEO over here. And you can learn how
to grow a YouTube channel with AI based
on what's working for me.
