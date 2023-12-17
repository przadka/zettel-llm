import os
import openai
import pandas as pd
import time
import ast


openai.api_key = os.getenv("OPENAI_API_KEY")

REQUESTS_PER_MINUTE = 10
SLEEP_INTERVAL = 60.0 / REQUESTS_PER_MINUTE

SYSTEM_MSG = '''
Assistant is a superhuman zettelkasten maintainer tasked with assigning keywords to zettels. This zettelkasten system covers a wide range of topics and is used by philosophers.

Example 1: 
===
Author: Hans Moravec
Title: "Robot: Mere machine to transcendent mind"
Quote: "The nonlinear equations of general relativity are notoriously hard to solve, only the simplest cases have been examined, and there is no theory of quantum gravity at all. That several plausible time machines have emerged in the bit of territory that has been explored is a hopeful indication that the vast unexplored vistas contain better ones, based more on subtle constructions than on brute-force spacetime bending."

Keywords assigned: theory of relativity, time travel
===

Example 2: 
===
Author: Susan Blackmore
Title: "The meme machine"
Quote: "Memes do not yet have precise copying machinery as DNA has. They are still evolving their copying machines, and this is what all the technology is for. […] [205] As Dawkins put it, the new replicator is “still drifting clumsily about in its primeval soup” (Dawkins 1976, p. 192). That soup is the soup of human culture, human artefacts, and human-made copying systems. You and I are living during the stage at which the replication machinery for the new replicator is still evolving, and has not yet settled down to anything like a stable form. The replication machinery includes all those meme-copying devices that fill my home, from pens and books to computers and hi-fi. […] Bearing in mind the dangers of comparing memes and genes, we can speculate that the same process works in both cases, producing a uniform high-fidelity copying system capable of creating a potentially infinite number of products. The genes have settled down, for the most part, to an exquisitely high-fidelity digital copying system based on DNA. The memes have not yet reached such a high-quality system and will probably not settle on one for a long time yet."

Keywords assigned: mind and body
===
'''

def assign_keywords(author, title, quote):
    """Assign new keywords using OpenAI."""
    
    # Construct the user message
    user_msg = f'''
Here is a new quote you need to assign keywords to:
===
Author: {author}
Title: "{title}"
Quote: "{quote}"
===

Possible keywords have been narrowed down to the following list, and they are sorted by relevance:

Possible keywords are:

===
Ab-grund
Akademia (Plato)
Amazon
America
American Civil War
American Declaration of Independence
American Revolution
Apple
Arab Spring
Arendtian principles
Austro-Hungarian Empire
Bible
Big Bang
Binding of Isaac
Brexit
Buddhism
COVID-19 pandemic
Catholicism versus Protestantism
Chile
China
Christianity
Citizens United v. Federal Election Commission
Cold War
Constitution of the United States of America
Copernican Revolution
Critique of Judgment (Kant)
Critique of Pure Reason (Kant)
Cuba
Cuban Missile Crisis
Drake equation
Dyson sphere
Easter Island
Egypt
Eichmann controversy
English Revolution
Europe
European Union
Euthyphro problem
Facebook
Fall of the Berlin Wall
Fermi paradox
French Revolution
GOFAI
Gaia hypothesis
Game of Life
Gerechtigkeit
God
Golden Rule
Google
Greece
Gödel’s incompleteness theorem
Habeas corpus
Haitian Revolution
Hellenistic philosophy
Hinduism
Hollywood
Hungarian Revolution
Inquisition
Internet
Iraq War
Islam
Islamism
Israeli-Palestinian conflict
Jesuits
Judaism
Lamarckian inheritance
Mach’s principle
Maoism
Maya
Me Too movement
Middle Ages
Milgram experiment
Moore’s law
Moore’s paradox
Nazism
Negro
Newcomb’s paradox
Nuremberg trials
Occident
Oedipus
Pascal’s wager
Poker
Presocratics
Pyrrhonism
Pythagoreanism
Reformation
Renaissance
Republic (Plato)
Roe v. Wade
Romanticism
Rome
Rorschach test
Russell’s paradox
Russia
Russian Revolution
Rwandan genocide
Régimen Militar (Chile)
SETI
Second World War
Semantic Web
Sendero Luminoso
Shoah
Sisyphos
Sittlichkeit
Soviet Union
Spanish Civil War
Stalinism
Star Trek
Star Wars
Stoicism
Switzerland
Tea Party
Third World
Trinity
Trojan War
Twitter
United Nations
United States Congress
United States of America
University of Oxford
Venezuela
Vienna
Vienna Circle
Vietnam War
Voynich manuscript
War in Afghanistan
War on Drugs
War on Terror
Warsaw Ghetto Uprising
What the Tortoise Said to Achilles (Carroll)
WikiLeaks
Yugoslav Wars
Zettelkasten
Zionism
abortion
absolute space
absolutism
academic freedom
action
active/passive
actually existing socialism
adoption
advertising
aestheticism
affirmative action
agon
agriculture
akrasia
alchemy
alcohol
algorithm
alienation
altermondialisme
alternative economy
altruism
amor fati
amor mundi
analog/digital
analytic/synthetic
anarchy
ancient ethics
animal husbandry
animal rights
anthropic principle
anti-consumerism
antiquity
antisemitism
ants
anything goes
aporia
archive
argos logos
argument from design
arrow of time
art
art of distinction
artificial intelligence
artificial life
artificial neural network
artistic creation
asceticism
assurance game
asylum
atheism
atom
authenticity
authority
autism
autonomous weapons
autonomy
avant-garde
ballistic missile submarine
ban
bare life
base and superstructure
basic income
beauty
bees
behaviorism
being
being and appearance
being and becoming
being and consciousness
being and thinking
bioethics
biopolitics
birds
birth control
black hole
body
bodybuilding
bourgeois/citizen
bureaucracy
camp
campaign finance reform
canon
capacity to do otherwise
capital punishment
capitalism
causa sui
causality
celibacy
centralization
chance
chaos
character
chastity
chess
chicken-and-egg problem
child sexual abuse
childbirth
children
chimpanzees
church
citizenship
city
civil rights
civil rights movement
civilian control of the military
civilization
class
class consciousness
class struggle
classless society
climate change
cloning
college
colonialism
comedy
common good
common sense
communism
communitarianism
compatibilism
computer
computer games
computer virus
concepts
conditional
conscience
consciousness
consensus
consent
consequentialism
conspiracy theory
constitution
constructivism
consumer society
contingency
continuum
copyright
corporation
corruption
cosmological argument
cosmopolitanism
council system
counterrevolution
courage
creatio ex nihilo
crime against humanity
critique
cryonics
cubism
culture
curiosity
cybernetics
cyberweapons
cyborg
cyclical versus linear conception of history
dance
death
death of God
debt
decision
deliberation
deliberative democracy
deliberative polling
democracy
deontology
depth and surface
desert
desire
determinism
development aid
dialectic
dialogue form
dictatorship
difference
différance
dignity
disability
disarmament
discipline
discourse ethics
disenchantment
division of labor
dolphins
domestic violence
domination
dream
drugs
dualism
duty
déconstruction
economic crisis
education
ego id super-ego
election by lot
elite
emancipation
emergence
empiricism
empiricism versus rationalism
empty slate
encryption
end of history
end of traditions
enemy
enlightenment
entailment
entertainment
envy
epistemology
epoché
equality
erweiterte Denkungsart
esotericism
essence
eternal recurrence
ethical naturalism
ethics
ethics of care
ethics of greatness
eudaimonia
eugenics
euthanasia
evangelicalism
event
evil
evil as a defect
evolution
evolution of cognition
evolution of death
evolution of humans
evolution of language
evolution of morality
evolution of religion
evolution of sexual reproduction
evolution of sleep
evolution of sociality
evolution of technology
evolutionarily stable strategy
evolutionary developmental biology
example
exception and rule
exclusion/inclusion
existentialism
experiment
expert
exploitation
expressionism
extinction
extra/ordinary
extraterrestrial life
fabrication
fact and fiction
facts and norms
failure
faith
fake news
false consciousness
family
fanaticism
fascism
fasting
fate
fear
federation
feelings
feminism
fetish
film
fine-tuning of the universe
first contact
fitness
football
foreign policy
forgiveness
form of government
formal logic
foundation
foundation myths
freaks
free market
freedom
freedom as absence of impediment
freedom of speech
freedom of the will
freedom of the will and natural causality as points of view
freedom of thought
freedom versus security
friendship
future
gambling
game
game theory
gene
genius
genocide
genre
geometric method
gift
globalization
goal
good and evil
grace
gravitation
greed
group selection
gun control
habit
hallucination
happiness
hate
health care reform
heaven and hell
hedonism
hermeneutic circle
hermeneutics
highest good
historical materialism
historical necessity
historicism
historiography
history
holiday
homeland
homelessness
homosexuality
hospitality
human being
human being and machine
human being as creator
human being as crown of creation
human being as inherently good or evil
human being as ruler over nature
human being versus animal
human enhancement
human rights
humaneness
humanism
humanitarian intervention
humanities
hylomorphism
hypocrisy
hysteria
ideal speech situation
ideal type
idealism
identity
identity of indiscernibles
identity politics
ideology
image
immanence/transcendence
immortality
immortality of the soul
immortality through fame
impartiality
imperialism
incest
incompatibilism
indexicals
induction
industrialization
inertia
inflation (cosmology)
informal logic
information
initiation rite
insects
intellect
intellectuals
interest
international law
intuition
jihad
joke
judging
just war
kairos
know-how/know-that
knowledge
labor
labor movement
language
large language models
laughter
law
law of nature
leader
learning
left/right
legitimacy
leisure
lex
liar paradox
liberalism
libertarianism (free will)
libertarianism (politics)
liberty and equality
life
life as a work of art
limits of formal logic
linguistic turn
literature
logic
logon didonai
logos
loneliness
lookism
love
lying
machine learning
magic
majority rule
manque à être
many-worlds interpretation
marriage
mask
mass
master and disciple
masturbation
materialism
mathematics
matter
matter life mind
meaning
meaning of life
means and end
medicine
medieval philosophy
meme
memory
men
mental illness
messianism
metaphor
metaphysics
military-industrial complex
mimesis
mind and body
mind uploading
miracle
mob
modern era
modernity
modesty
money
monism
moral sentiments
morality
motherhood
mountaineering
multiverse
music
mutually assured destruction
mysticism
myth
natality
nation state
nationalism
natural right
naturalism
nature
nature versus culture
nature versus nurture
necessity
necessity of the life process
negation
negative theology
neo-Aristotelianism
neo-Kantianism
neoliberalism
nihilism
nomos
non-conceptual content
non-governmental organizations
nonviolent resistance
nothingness
novel
nuclear weapons
objectivity
old age
ontological argument
ontology
open source
opera
opinion
origin
origin of life
original and copy
original sin
overdetermination
overpopulation
pacemaker
pacifism
pantheism
paradigm
paradox
paranoia
parenthood
particularism
parts and whole
party
passion for distinction
past
paternalism
patriarchy
pedophilia
penis envy
people
perfectionism
performative self-contradiction
performative speech acts
permanent revolution
person
personal identity
petroleum
pharmaceutical industry
phenomenology
philosophy
philosophy as a system
philosophy versus science
photography
physicalism
physics
pity
placebo effect
plagiarism
pleasure and pain
plebiscite
plurality of human beings
poetry
police
polis
political economy
political philosophy
political representation
politics
popular sovereignty
pornography
possibility
possible world
posthumanism
postmodernity
potentiality and actuality
poverty
power
practical reason
practice
prayer
precedent
presence/absence
preventive war
primitive peoples
principle of double negation
principle of non-contradiction
principle of publicity
principle of sufficient reason
principles
prison
prisoner’s dilemma
private military company
probability theory
problem of complexity
problem of evil
problem of foundation
problem of pluralism
problem of scale
problem of universals
proceduralism
process
professional revolutionary
progress
project
promise
proof of an external world
proof of the existence of God
proper name
property
proposition
prostitution
protection of the environment
protests of 1968
psychoanalysis
psychosis
psychotherapy
public happiness
public opinion
public reason
public sphere
public transport
public/private
punctuated equilibrium
punishment
pure versus applied science
quantum computer
quantum mechanics
racism
radical evil
rape
rational choice theory
rave
reactionary
reading
realism (arts)
realism (politics)
rearing of children by the state
reason
reason versus faith
reason versus intellect
reason versus passion
reason versus sense perception
recycling
reductio ad absurdum
reform or revolution
refugee
regulative idea
reification
relation
relationship between politics and economy
relativism
religion
renewable energy
repetition
representation
representative democracy
repression
republic
research
resistance
respect
responsibility
retroactivity
revenge
revolution
rhetoric
right
right of the strongest
risk society
rule-following
sacrifice
scapegoat
schizophrenia
school
science
science fiction
science versus religion
scientific revolution
secessio plebis
second law of thermodynamics
secret police
secret service
sects
secularization
self-consciousness
self-driving cars
self-help
self-preservation
self-reference
self-respect
selflessness
sense
sense perception
separation of church and state
separation of powers
serial killer
sexual difference
sexuality
shame
signifier
simulation hypothesis
singularity
skepticism
slavery
sleep
smartphone
social contract
socialism
socialist realism
society
society as body
solidarity
solipsism
sophistry
soul
sovereignty
space
space travel
spacetime
species
spirit of the revolution
splitting
state
state of nature
statelessness
story
strike
string theory
structuralism
struggle between the sexes
struggle for recognition
subject
sublimation
substance
suicide
superhero
superintelligence
supervenience
surfing
surrealism
surrogacy
surveillance state
systems theory
taste
technology
teleology
territory
terror
terrorism
thaumazein
the absolute
the absolutely other
the absurd
the death of Man
the good
the infinite
the lesser evil
the new
the present
the real
the self
the unconscious
the unspeakable
theater
theory and practice
theory of everything
theory of relativity
thinking
time
time travel
tobacco
tolerance
torture
totalitarianism
trade union
tradition
tragedy
transcendental
transhumanism
translation
trust
truth
truth as coherence
truth as correspondence
truth as disclosure
truth as what works
twins
tyranny
tyranny of the majority
uncertainty principle
understanding
unemployment
unidentified flying object
unity
unity of science
universal suffrage
universalism
university
use and exchange value
usury
utilitarianism
utopia
vacuum
vagueness
value
vampire
vegetarianism
verse
vertigo
violence
virtual
virtual reality
virtue
virtue ethics
vitalism
von Neumann probe
war
war crime
wealth
welfare state
whales
will
wireheading
witch hunt
witches
women
world
world state
worldlessness
writing
xenophobia
youth
zoo hypothesis
===

Please assign keywords to the new quote. Use only the keywords from the list above. Assign between one and three keywords, separated by commas. Output only the keywords, nothing else. Sort keywords from the most relevant to the least relevant.

Thank you in advance!
'''

    print(f"System message: {SYSTEM_MSG}")
    print(f"User message: {user_msg}")

    try:
        response = openai.ChatCompletion.create(
            model='gpt-4-1106-preview',
            messages=[
                {"role": "system", "content": SYSTEM_MSG},
                {"role": "user", "content": user_msg}
            ],
            max_tokens=30,
            temperature=0.0,
        )
        
        return response['choices'][0]['message']['content'].strip()

    except openai.error.InvalidRequestError as e:
        print(f"Error while processing the request: {e}")
        return "ERROR_TRIGGERED_CONTENT_MANAGEMENT_POLICY"


def main():
    """Main function to process queries."""

    df = pd.read_csv("queries.csv")
    # add new column to the dataframe to store the assigned keywords, type is string

    df["Big Context Keywords"] = ""

    for index, row in df.iterrows():
        print(f"Processing row {index}...\n")
        author = row["author(s)"]
        title = row["title of the source"]
        quote = row["quotation"]
        assigned_keywords = assign_keywords(author, title, quote)
        print(f"Assigned keywords: {assigned_keywords}")
        # write assigned keywords to the dataframe, under the column "Assigned Keywords"
        df.at[index, "Big Context Keywords"] = assigned_keywords
        print("\n")

        # Sleep for the calculated interval to respect the rate limit
        time.sleep(SLEEP_INTERVAL)

    # Save the dataframe with assigned labels back to a new CSV
    df.to_csv("queries.csv", index=False)



if __name__ == "__main__":
    main()