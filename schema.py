import graphene
from graphene import Field, String, Int, List, Mutation
from models import db, Genre, Movie

# Define Genre type for GraphQL
class GenreType(graphene.ObjectType):
    id = Int()
    name = String()

# Define Movie type for GraphQL
class MovieType(graphene.ObjectType):
    id = Int()
    title = String()
    description = String()
    release_year = Int()
    genres = List(GenreType)

# Mutation to create a genre
class CreateGenre(Mutation):
    class Arguments:
        name = String(required=True)

    genre = Field(lambda: GenreType)

    def mutate(self, info, name):
        # Input validation: Name should not be empty or too long
        if not name or len(name) > 100:
            raise Exception("Invalid genre name.")
        
        genre = Genre(name=name)
        db.session.add(genre)
        db.session.commit()
        return CreateGenre(genre=genre)

# Mutation to update a genre
class UpdateGenre(Mutation):
    class Arguments:
        id = Int(required=True)
        name = String(required=True)

    genre = Field(lambda: GenreType)

    def mutate(self, info, id, name):
        genre = Genre.query.get(id)
        if not genre:
            raise Exception("Genre not found.")
        
        if not name or len(name) > 100:
            raise Exception("Invalid genre name.")

        genre.name = name
        db.session.commit()
        return UpdateGenre(genre=genre)

# Mutation to delete a genre
class DeleteGenre(Mutation):
    class Arguments:
        id = Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        genre = Genre.query.get(id)
        if not genre:
            raise Exception("Genre not found.")
        
        db.session.delete(genre)
        db.session.commit()
        return DeleteGenre(success=True)

# Query to get movies by genre
class GetMoviesByGenre(graphene.ObjectType):
    movies = List(MovieType, genre_id=Int(required=True))

    def resolve_movies(self, info, genre_id):
        genre = Genre.query.get(genre_id)
        if not genre:
            raise Exception("Genre not found.")
        
        return genre.movies  # Access the related movies

# Query to get genres by movie
class GetGenresByMovie(graphene.ObjectType):
    genres = List(GenreType, movie_id=Int(required=True))

    def resolve_genres(self, info, movie_id):
        movie = Movie.query.get(movie_id)
        if not movie:
            raise Exception("Movie not found.")
        
        return movie.genres  # Access the related genres

# Root query that includes all the query types
class Query(graphene.ObjectType):
    get_movies_by_genre = Field(GetMoviesByGenre)
    get_genres_by_movie = Field(GetGenresByMovie)

# Mutation class to wrap all mutations for genre management
class GenreMutations(graphene.ObjectType):
    create_genre = CreateGenre.Field()
    update_genre = UpdateGenre.Field()
    delete_genre = DeleteGenre.Field()

class Mutation(graphene.ObjectType):
    genre_mutations = Field(GenreMutations)

# Complete schema definition
schema = graphene.Schema(query=Query, mutation=Mutation)
