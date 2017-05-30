import fresh_tomatoes
import media

#creating movie objects
guardians_of_the_galaxy = media.Movie("Guardians of the Galaxy",
                                    "https://upload.wikimedia.org/wikipedia/en/thumb/8/8f/GOTG-poster.jpg/220px-GOTG-poster.jpg",
                                    "https://www.youtube.com/watch?v=d96cjJhvlMA")

doctor_strange = media.Movie("Doctor Strange",
                            "https://upload.wikimedia.org/wikipedia/en/thumb/c/c7/Doctor_Strange_poster.jpg/220px-Doctor_Strange_poster.jpg",
                            "https://www.youtube.com/watch?v=HSzx-zryEgM")

hobbit_unexpected_journey = media.Movie("The Hobbit: An Unexpected Journey",
                                        "https://upload.wikimedia.org/wikipedia/en/b/b3/The_Hobbit-_An_Unexpected_Journey.jpeg",
                                        "https://www.youtube.com/watch?v=SDnYMbYB-nU")

hobbit_desolation_of_smaug = media.Movie("The Hobbit: The Desolation of Smaug",
                                        "https://upload.wikimedia.org/wikipedia/en/4/4f/The_Hobbit_-_The_Desolation_of_Smaug_theatrical_poster.jpg",
                                        "https://www.youtube.com/watch?v=Os1G8RtqY2c")

hobbit_five_armies = media.Movie("The Hobbit: The Battle of the Five Armies",
                                "https://upload.wikimedia.org/wikipedia/en/0/0e/The_Hobbit_-_The_Battle_of_the_Five_Armies.jpg",
                                "https://www.youtube.com/watch?v=iVAgTiBrrDA")

#adding them to a list
movies = [guardians_of_the_galaxy, doctor_strange, hobbit_unexpected_journey, hobbit_desolation_of_smaug, hobbit_five_armies]

#opening movie trailer page
fresh_tomatoes.open_movies_page(movies)
