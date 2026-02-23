Simple Leaderboard service:

Leaderboard service operations:


USER: {
    UserName: Str
    UserId: UUID
    Score: int
}

CreateUser POST {UserName} -> {UserId}
    Creates a user with user name and returns the users id

UpdateScore POST {UserId, score} -> Message
    Updates the score of the user with the provided score, returns success state

GetTopXScores GET {X: int} -> Rows
    Gets the topX or up to X rows from the database in descending order

GetUserContext GET {UserId} -> {User, User, User}
    Returns the user context in the following format: {Above user, Requested User, Below User}