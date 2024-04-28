class PIXAR_Prompt(object):
    path2IC_prompt = '''### Paths:
User YM_4944 received a recommendation for the movie "The Empire Strikes Back" through the following paths.
YM_4944 -> user likes item -> Independence Day -> item has genres as attribute: -> Action -> attribute is genres of item: -> The Empire Strikes Back
YM_4944 -> user likes item -> Independence Day -> item has genres as attribute: -> Action -> attribute is genres of item: -> The Empire Strikes Back -> item has release year as attribute: -> 1980's -> attribute is release year of item: -> The Empire Strikes Back

### Context:
The Empire Strikes Back.
The actors of the movie is/are Harrison Ford Kenny Baker Alec Guinness Frank Oz David Prowse Billy Dee Williams Peter Mayhew Mark Hamil Carrie Fisher Mark Hamill Anthony Daniels.
The release_year of the movie is/are 1980's.
The genres of the movie is/are Action Science Fiction Fantasy Thriller Adventure.
The directors of the movie is/are Irvin Kershner.

### Instruction:
Use the Context information and path information to create a useful context that can be helpful when explaining the reason for the recommendation for the user YM_4944.
The given information could include uncertain information, please do NOT include uncertain information.
Respond in SHORT and CONCISE language. Your response should be WITHIN 50 words.

### Response:
YM_4944 enjoys movies like *Independence Day* which share genres with *The Empire Strikes Back* such as Action, Science Fiction, Fantasy, and Adventure. The recommendation of *The Empire Strikes Back* is based on its similar action-packed and adventurous genres and its acclaimed direction by Irvin Kershner.

### Paths:
User YM_1762 received a recommendation for the movie "Alien" through the following paths.
YM_1762 -> user likes item -> L.A. Confidential -> item has genres as attribute: -> Thriller -> attribute is genres of item: -> Alien
YM_1762 -> user likes item -> The Texas Chainsaw Massacre -> item has release year as attribute: -> 1970's -> attribute is release year of item: -> Alien -> item has directors as attribute: -> Ridley Scott -> attribute is directors of item: -> Alien

### Context:
Alien.
The actors of the movie is/are John Hurt [Kane] Sigourney Weaver [Ripley] Veronica Cartwright Tom Skerritt Ian Holm Yaphet Kotto Harry Dean Stanton.
The directors of the movie is/are Ridley Scott.
The genres of the movie is/are Thriller Fantasy Science Fiction.
The release_year of the movie is/are 1970's.

### Instruction:
Use the Context information and path information to create a useful context that can be helpful when explaining the reason for the recommendation for the user YM_1762.
The given information could include uncertain information, please do NOT include uncertain information.
Respond in SHORT and CONCISE language. Your response should be WITHIN 50 words.

### Response:
YM_1762 enjoys films like *L.A. Confidential* and *The Texas Chainsaw Massacre* which share attributes with *Alien*. The recommendation of *Alien* is based on its Thriller and Science Fiction genres, similar to *L.A. Confidential*, and its 1970s release and direction by Ridley Scott, akin to *The Texas Chainsaw Massacre*.

### Paths:
User {user} received a recommendation for the movie "{item}" through the following paths.
{paths}

### Context:
{item}.
{item_information}

### Instruction:
Use the Context information and path information to create a useful context that can be helpful when explaining the reason for the recommendation for the user {user}.
The given information could include uncertain information, please do NOT include uncertain information.
Respond in SHORT and CONCISE language. Your response should be WITHIN 50 words.

### Response:
'''
    IC2explanation_prompt = '''### Context:
YM_4944 enjoys movies like *Independence Day* which share genres with *The Empire Strikes Back* such as Action, Science Fiction, Fantasy, and Adventure. The recommendation of *The Empire Strikes Back* is based on its similar action-packed and adventurous genres and its acclaimed direction by Irvin Kershner.

### Record:
The history films watched by the user YM_4944 are:
1: Money Talks
The actors of the movie is/are Michael Wright Damian Chapa Larry Hankin Paul Gleason Heather Locklear Charlie Sheen Gerard Ismael Daniel Roebuck Elise Neal Veronica Cartwright David Warner Paul Sorvino Chris Tucker.
The genres of the movie is/are Comedy.
The release_year of the movie is/are 1990's.
The directors of the movie is/are Brett Ratner Brent Ratner.
2: Twister
The actors of the movie is/are Bill Paxton Jami Gertz Alan Ruck Lois Smith Zach Grenier Joey Slotnick Sean Whalen Helen Hunt Cary Elwes Scott Thomson Philip Seymour Hoffman.
The genres of the movie is/are Action Adventure Thriller.
The directors of the movie is/are Jan De Bont.
The release_year of the movie is/are 1990's.
3: Ghost
The actors of the movie is/are Vincent Schiavelli Rick Aviles Whoopi Goldberg Tony Goldwyn Demi Moore Patrick Swayze.
The genres of the movie is/are Drama Comedy Romance Thriller.
The release_year of the movie is/are 1990's.
The directors of the movie is/are Jerry Zucker.
4: Scary Movie
The actors of the movie is/are Anna Faris Shawn Wayans Shannon Elizabeth Marlon Wayans Dave Sheridan Cheri Oteri Jon Abrahams Kurt Fuller David L. Lander Lochlyn Munro Carmen Electra Regina Hall.
The genres of the movie is/are Suspense Horror Comedy.
The release_year of the movie is/are 2000's.
The directors of the movie is/are Keenen Ivory Wayans.
5: Independence Day
The actors of the movie is/are James Rebhorn James Duval Nectar Rose Bill Pullman John Storey Andrew Keegan Harvey Fierstein Robert Loggia Will Smith Vivica A. Fox Harry Connick Mary McDonnell Jeff Goldblum Judd Hirsch Margaret Colin Julie Moran Randy Quaid.
The genres of the movie is/are Action Science Fiction Adventure Thriller Fantasy.
The release_year of the movie is/are 1990's.
The directors of the movie is/are Roland Emmerich.
6: Back to the Future
The actors of the movie is/are Harry Waters Jr. Billy Zane Claudia Wells Lea Thompson Jason Hervey Christopher Lloyd Crispin Glover Lee McCain Casey Siemaszko Thomas F. Wilson Michael J. Fox Wendie Jo Sperber George DiCenzo James Tolkan Marc McClure.
The genres of the movie is/are Comedy.
The release_year of the movie is/are 1980's.
The directors of the movie is/are Robert Zemeckis.

### Instruction:
As a recommender system in the movie domain, based on reasonable recommendation path based Context, YM_4886's historical viewing records and historical viewing movie information., tell YM_4886 why he or she needs to watch this movie, and what are the advantages of this movie.
Give reasons why YM_4944 needs to watch this movie with the following title and class:
The Empire Strikes Back.
The actors of the movie is/are Harrison Ford Kenny Baker Alec Guinness Frank Oz David Prowse Billy Dee Williams Peter Mayhew Mark Hamil Carrie Fisher Mark Hamill Anthony Daniels.
The release_year of the movie is/are 1980's.
The genres of the movie is/are Action Science Fiction Fantasy Thriller Adventure.
The directors of the movie is/are Irvin Kershner.

Use ONLY the information mentioned above. You're responding to YM_4944. Directly tell YM_4944 the reason.
Respond in SHORT and CONCISE language. Your response should be WITHIN 150 words and 3 different reasons.

### Response:
YM_4944, based on your movie preferences, here are compelling reasons to watch *The Empire Strikes Back*:

1. **Aligned Genres**: You enjoyed *Independence Day*, which shares the Action, Science Fiction, Fantasy, and Adventure genres with *The Empire Strikes Back*. This similarity in genre provides a thrilling and immersive experience that you have appreciated in the past.

2. **Stellar Cast and Acclaimed Direction**: The movie features iconic performances by Harrison Ford, Mark Hamill, and Carrie Fisher under the skilled direction of Irvin Kershner. This combination enhances the storytelling quality and character depth, offering a more engaging and memorable viewing experience.

3. **Classic and Impactful Storytelling**: As a sequel in the original Star Wars trilogy, this film expands on the epic saga with a deep narrative and complex relationships, paired with high-stakes adventure and rich, fantastical elements that resonate with your tastes in impactful, story-driven cinema.

*The Empire Strikes Back* is not just a film but an experience that aligns well with your cinematic tastes and preferences for genre and quality.

### Context:
{context}

### Record:
{record}

### Instruction:
As a recommender system in the movie domain, based on reasonable recommendation path based Context, {user}'s historical viewing records and historical viewing movie information., tell YM_4886 why he or she needs to watch this movie, and what are the advantages of this movie.
Give reasons why {user} needs to watch this movie with the following title and class:
{item}.
{item_information}

Use ONLY the information mentioned above. You're responding to {user}. Directly tell {user} the reason.
Respond in SHORT and CONCISE language. Your response should be WITHIN 150 words and 3 different reasons.

### Response:
'''