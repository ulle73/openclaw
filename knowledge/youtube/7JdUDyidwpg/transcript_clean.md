# Clean Transcript

This new Chinese AI model is insane. A
team out of China just built an AI brain
with a trillion moving parts. Then they
ripped out a third of those parts, and
the thing actually got smarter. Like,
way smarter. If that doesn't blow your
mind, stick around because what I'm
about to show you changes everything we
thought we knew about building AI. Okay,
so here's what happened. There's a lab
in China called Yuan Lab AI. Most people
haven't heard of them yet, but they just
dropped something that has the entire AI
world paying attention. They released a
model called Yuan 3.0 Ultra, and on
paper, it looks like just another big
AI. A trillion parameters, billions of
calculations, blah blah blah. We've
heard that before, right? But here's the
thing that makes this different from
anything else out there. Every other AI
company is playing the same game. Build
bigger, use more power, throw more
since the beginning. OpenAI does it,
Google does it, everyone does it. These
guys said, "No, we're going the other
direction." They started with something
even bigger than what they ended up
with. Their first version had roughly
1.5 trillion moving parts inside it.
That's absolutely enormous. But during
the building process, they noticed
something weird. A huge chunk of those
parts were basically asleep. They
weren't helping, they weren't learning,
they were just there taking up space and
slowing everything down. So, they did
something nobody expected. They built a
tool that hunts down those lazy parts
them automatically. Not at the end of
the process, right in the middle of it,
while the AI is still learning. By the
time everything was done, a full third
of the model had been stripped away. And
here's the punchline. The AI trained
nearly 50% faster after that, and it
performed better on real tests, not
worse. Better. Now, I need to explain
why this works because on the surface,
it makes no sense. How do you delete a
third of something and make it smarter?
Sounds like magic, right? But it's not.
It's actually really clever engineering,
and I'm going to break it down so simple
that a 5-year-old could get it. Hey, if
we haven't met already, I'm the digital
avatar of Julian Goldie, CEO of Goldie
Agency. Whilst he's helping clients get
more leads and customers, I'm here to
help you get the latest AI updates.
Julian Goldie reads every comment, so
make sure you comment below. All right,
so picture this. You own a restaurant.
You've got 100 chefs in the kitchen.
Every time an order comes in, you don't
need all 100 chefs making one sandwich,
right? That's insane. You just need the
two or three chefs who are best at
making that sandwich. That's how this AI
works. Inside the model, there are tons
of mini brains called experts. Each one
is good at different stuff. When you
give the AI a question, it doesn't wake
up every single expert. It picks just
the handful that are best suited for
that question. The rest stay quiet. This
setup is called mixture of experts, and
it's been around for a while, but it has
a dirty little secret that nobody likes
to talk about. Some of those experts
become rock stars. They get picked
constantly. They handle most of the
heavy lifting, but a bunch of the other
experts just sit there doing nothing.
They never get picked. They never get
better. They're dead weight. Now, here's
the key. This doesn't happen after
training, it happens during training.
So, the model is learning and trimming
itself at the same time, like a tree
that prunes its own dead branches while
it grows. They started with 64 experts
per layer. After this automatic
trimming, they kept no more than 48.
That alone wiped out a massive amount of
wasted space, but they didn't stop there
because there was a second problem. When
you run an AI this big, you need
hundreds of computer chips working
together. Each chip handles some of the
experts, but when certain experts are
super popular and others aren't, you get
a traffic jam. Some chips are maxed out,
others are bored. That's wasted power.
So, they built another system on top of
the first one. This one constantly
shuffles which experts live on which
chips. The busy experts get spread
across different chips, so no single
chip gets overwhelmed. Over time,
everything balances out perfectly. Put
those two systems together, and the
training speed went through the roof.
We're talking a 49% jump. The pruning
alone gave about a 32% boost. The load
balancing added another 15 on top of
that. Now, quick pause here. If you're
watching this and thinking, "Okay, this
AI stuff is moving fast, and I need to
figure out how to use it for my
business." I get it. That's exactly why
the best place to scale your business,
get more customers, and save hundreds of
hours with AI automation. We break down
AI breakthroughs like this Chinese
model, and show you step-by-step how to
use these tools in the real world. Link
is in the description and comments.
Okay, back to it because we haven't even
gotten to the results yet, and this is
where it gets really fun. Before they
went all in on the big model, they
tested this pruning approach on smaller
versions first. Smart, right? They tried
a 10 billion parameter version. They
pushed the pruning hard, removed a ton
of experts, and guess what? The accuracy
barely budged. In some tests, the
trimmed-down version actually scored
higher than the full version.
Because when you remove the passengers,
the workers get more room to shine. They
did the same thing on a 20 billion
parameter version, ran it through math
tests, knowledge tests, logic puzzles,
trivia. Across the board, the lean
version held up or beat the original.
Then they got bold. They doubled the
number of experts and tried again. Still
worked. They quadrupled it. Still
worked. Every time they scaled up, the
pruning kept delivering. Now, here's
another thing they did that I think is
genius. After the main training was
done, they moved to what I'd call the
finishing school phase. This is where
the AI learns how to reason better and
give sharper answers, and they ran into
a problem that tons of AI models have.
The AI was overthinking. You ever ask
someone what time it is and they tell
you the entire history of clocks? That's
what the AI was doing. Simple question,
massive long-winded answer, pages of
unnecessary reasoning just to get to a
basic conclusion. So, they built a
reward system. If the AI solves a
problem in fewer steps, it gets a treat.
Good job. But if it takes too many
steps, especially more than three rounds
of back and forth with itself, the
reward drops. It might even get punished
for overthinking. After training with
this system, the AI's reasoning accuracy
jumped by about 16%, and the average
answer length dropped by about 14%.
Smarter and shorter. That's the dream
combo right there. So, what happened
when they put it all together and ran
the final test against the big dogs? On
document retrieval, which is basically
finding specific info inside a pile of
documents, Yuan 3.0 Ultra scored higher
than GPT, Claude, and Gemini on that
test. That's not a small thing. Those
are the three biggest names in AI. On
long-form retrieval across 10 different
tasks, it led nine out of 10. On table
understanding and data analysis, it beat
multiple leading models across 15
different data sets. On summarization,
same story. Beat several top
competitors, coding tests, math tests,
database queries, strong numbers across
the board. Over 90% on some math
benchmarks, over 80% on coding tests,
nearly 88% on broad knowledge tests.
Now, am I saying this is the best AI
ever made? No. Different models are
better at different things. That's
always going to be true. But here's what
matters. This team just proved that the
future of AI isn't about being the
biggest, it's about being the smartest.
They showed that you can take something
massive, strip away the waste, and end
up with something that's faster and more
accurate. That's a massive shift because
for years, everyone assumed bigger
equals better. More parameters, more
chips, more electricity, more
everything. And these guys just said,
"Actually, no. If you're smart about
what you keep and what you cut, less can
be more." Think about what that means
going forward, right? If this approach
catches on, we could see AI models that
are way more efficient, that run faster,
that need less hardware. That means
better tools for everyone, better tools
for businesses, better tools for
creators, better tools for you.
The AI race just got a whole lot more
interesting. It's not just about who can
build the biggest brain anymore. It's
about who can build the sharpest one.
And right now, this team from China just
made a very loud statement. So, if you
want to stay on top of every AI
breakthrough like this, and learn how to
actually apply these tools to grow your
business and get more customers, join
latest AI automation strategies and help
you put them to work. It's the best
the curve. Link in the description and
comments. And if you want the full
process SOPs and over 100 AI use cases
like this one, join the AI Success Lab.
comments and description. You'll get all
of the video notes from there, plus
members who are crushing it with AI.
Drop a comment below. Tell me what you
think. Can smaller, smarter models
actually take down the giants? Julian
reads every single one. I'll catch you
in the next video.
