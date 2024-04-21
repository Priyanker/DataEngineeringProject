from django.shortcuts import render
from .openweatherapi import WeatherMovieRecommender

def get_movie_recommendations(request):
    if request.method == "POST":
        city = request.POST.get('city')
        recommender = WeatherMovieRecommender(city)
        weather_data = recommender.get_weather_data()
        movie_recommendations_list = recommender.generate_movie_recommendations()
        return render(request, 'recommendations/movies.html', {'movie_recommendations_list': movie_recommendations_list, 'weather_data': weather_data})
    return render(request, 'recommendations/index.html')
