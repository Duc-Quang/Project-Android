package com.example.w6.rest

import com.example.w6.movie.MovieResp
import retrofit2.http.GET
import retrofit2.http.Query

/**
 * Created by nampham on 5/10/21.
 */
interface MovieDBService {

    @GET("movie/now_playing")
    suspend fun listNowPlayMovies(
        @Query("language") language: String, @Query("page") page: Int,
    ): MovieResp

    ///movie/upcoming
    @GET("movie/upcoming")
    suspend fun listUpComingMovies(
        @Query("language") language: String,
        @Query("page") page: Int,
    ): MovieResp
}