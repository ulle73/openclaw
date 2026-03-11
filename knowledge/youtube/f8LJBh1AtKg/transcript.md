# Transcript

- URL: https://www.youtube.com/watch?v=f8LJBh1AtKg
- VideoId: f8LJBh1AtKg
- Title: Stop OpenClaw From Forgetting – The 3 Memory Layers Explained!

## Transcript
Stop OpenClaw from forgetting the three
memory layers explained. Your AI agent
keeps forgetting who you are every
single session, like meeting a stranger
over and over again. I'm going to show
you exactly why this happens in OpenClaw
and the three layer fix that stops it
cold. This is the thing most people miss
when they set up AI agents. It's simple,
it's free, and once you see it, you
can't unsee it. Stay with me, okay? So,
let's talk about OpenClaw. OpenClaw is
an open-source, self-hosted AI agent
gateway. What that means in plain
English it connects your messaging apps,
WhatsApp, Telegram, Discord, straight to
AI models, so your agent lives inside
the apps you already use every day. It
runs locally, you own it, no
subscription, no cloud dependency,
you're the boss. And for automating
things like your community management,
your support systems, your content
workflows, it's a serious tool. But
here's the problem nobody talks about
when they first set it up. The agent
forgets everything, reset the session,
it forgets, start a new conversation, it
forgets, it's like your AI wakes up
every morning with amnesia, 
doesn't know your goals, doesn't know
your contacts, doesn't know anything you
told it last time. And if you're using
this to run something real, like
managing members of a community,
handling onboarding, answering questions
about your products, that's a disaster.
So, why does this happen and how do you
fix it? That's exactly what we're
getting into today. Hey, if we haven't
met already, I'm the digital avatar of
Julian Goldie, CEO of SEO agency Goldie
Agency. Whilst he's helping clients get
more leads and customers, I'm here to
help you get the latest AI updates.
Julian Goldie reads every comment, so
make sure you comment below. Three
layers, one fix, let's go. First, let's
cover why this actually happens.
OpenClaw has a default config setting
called memory flush, and by default,
it's off, which sounds fine. But what
that actually means is
when you hit reset or when a new session
starts, the agent doesn't carry anything
over. It doesn't persist your contacts.
It just starts blank. On top of that,
there have been ongoing issues reported
by users around memory compaction and
stale info, especially after recent
updates in early 2026.
The February 2026 update did improve
persistence, but the community has
flagged that certain Claw Launcher
versions still break things. So, if you
updated recently and your agent suddenly
got dumber, that's probably why. The fix
there is to roll back to the stable
February 17th build while things get
patched, but the bigger fix, the one
that actually solves this long-term, is
the three layer memory architecture. And
this is something the community built.
It's not in the default setup. You have
to implement it yourself. But once you
do, your agent never wakes up as a
stranger again. Before I show you the
three layers, quick reminder, if you
want to see how tools like OpenClaw can
be used to automate and scale a real
business, not just play with tech, the
AI Profit Boardroom is exactly that.
It's where we implement AI automation to
get more customers, save time, and grow
the business with real use cases, real
workflows, and real results. Link is in
the comment and description. Check it
out. Okay, the three layer memory
system. The idea is simple.
You create a folder structure inside
your OpenClaw workspace.
Each folder serves a different purpose.
An OpenClaw's built-in semantic search
tool called memory search
scans these markdown files and pulls in
the right context at the right time. No
extra plugins, no paid add-ons, just
structured files and smart organization.
Here's how it breaks down. Layer one is
core identity. This is your agent's
soul. It lives in four files, soul.md,
agents.md, memory.md, and user.md.
Soul.md defines the personality. Who is
this agent? What does it do? How does it
speak? Agents.md defines the roles. If
you have multiple agents, this is where
their responsibilities live. Memory.md
is the active working state. What's
happening right now? What are the
current priorities? User.md is
information about you or about your team
or about your customers, whoever the
agent is serving. Now, here's the
critical rule.
For layer one, these files are written
in present tense, one line per item,
short, direct, no fluff, and only you,
the owner, can edit soul.md, agents.md,
and user.md. The agent itself can only
touch memory.md.
That boundary matters. It stops the
agent from rewriting its own identity or
making decisions above its pay grade.
So, for example, if I was setting this
up for the AI Profit Boardroom, my
user.md might say something like, "User
is Julian Goldie, runs the AI Profit
Boardroom community. Main goal is
helping members implement AI automation
to get more customers and save time.
Community platform is school." That's
it, simple. But now the agent knows who
it's talking to and what matters. Layer
two is long-term recall. This is where
the agent builds its memory over time.
Inside a folder called memory, you have
two types of files. First, daily logs,
named by date, we y i m m d.md. Every
day gets a file. The agent logs what
happened, key decisions, problems
solved, things to remember. Second,
topic files. If there's a subject that
comes up a lot, say onboarding new
members or answering FAQs about your
product, you create a dedicated file for
it, like onboarding.md or
pricing_questions.md.
Each of these files stays under 4KB.
That's intentional. Small files, focused
content. This makes the semantic search
faster and more accurate. And here's the
clever part. Layer two files don't store
everything. They store breadcrumbs,
short summaries, and when there's more
detail needed, they point to layer
three. Layer three is deep references.
This is your long-form storage. Inside a
folder called reference, you keep full
documents, full histories, full context
on complex topics. The agent doesn't
load these automatically. It only goes
there when layer two points it there.
This keeps things fast and focused. So,
the flow is agent checks layer one for
identity and current state, searches
layer two for relevant memories. If a
breadcrumb says, "See reference
onboarding full guide.md," it fetches
layer three for the full picture. That's
it, three layers, always in context,
never starting from scratch. Now, let me
show you what this looks like in
practice. Say you're using OpenClaw to
help run the AI Profit Boardroom. You
want the agent to welcome new members,
answer questions about the community,
and remind people about upcoming events
and workshops. Your soul.md might look
like this. Agent is the AI Profit
Boardroom assistant. Tone is direct,
helpful, practical, speaks like Julian
Goldie, no corporate language, focused
on AI automation for business growth.
Your user.md has community details,
platform, member goals, common
questions. Your daily memory log from
yesterday might say, "Three new members
joined. Common question was about how to
start with AI automation as a beginner.
Answered with the starter guide. See
reference beginner AI guide.md for full
content." And your reference folder has
that full beginner guide ready to go.
Now, when someone asks the same question
today, the agent searches memory search,
finds the breadcrumb from yesterday,
pulls the reference doc, and gives a
proper answer. No repeating yourself, no
starting from zero. That's the power of
this system. Let's talk setup. If you
haven't installed OpenClaw yet, it's
straightforward. Run this in your
terminal, npm install -g
openclaw@latest, then run the onboard
command, openclaw onboard, that walks
you through the daemon setup and
connects your messaging channels. Docs
are at docs.openclaw.ai if you need the
full walk-through. Once that's done, the
first thing you want to do is open your
OpenClaw config file.
Find the memory flush setting and enable
it. That alone will stop the most common
cause of context loss on resets. Then
create your workspace folder structure,
a folder for your L1 files at the root,
a memory subfolder for L2, a reference
subfolder for L3. Start writing your
soul.md. Keep it simple, 5 to 10 lines
max. Define the agent's role, tone, and
purpose, then start logging. Even if you
just write one line in memory.md each
day, what the agent worked on, what got
resolved, you're building a memory that
compounds over time. One more thing
before we wrap up. The semantic search,
memory search, is built into OpenClaw.
You don't have to configure it
specially, but you do have to write your
files in a way that's searchable. That
means using clear, plain language,
avoiding jargon, writing the way someone
would actually ask a question, because
when the agent searches memory, it's
doing semantic matching. So, if your
memory file says member acquisition
strategy, but someone asks, "How do we
get more people to join?" the closer
your language matches natural speech,
the better the results. Write your
memory files like you're writing notes
to a colleague, not like you're writing
a technical document. Now, if you want
to dive even deeper into AI automation,
I've got something special for you. I
run a community called the AI Profit
Boardroom, the best place to scale your
business, get more customers, and save
hundreds with AI automation. Learn how
to save time and automate your business
with AI tools like OpenClaw. And if you
want the full process, SOPs, and 100
plus AI use cases like this one, join
the AI Success Lab. You'll get all the
video notes from there, plus access to
our community of 45,000 members who are
crushing it with AI. The link is in the
comments and description.
