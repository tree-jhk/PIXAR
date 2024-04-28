class LLMXRec_Prompt(object):
    explanation_prompt = '''### Record:
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