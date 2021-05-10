package com.example.w6

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.w6.rest.RestClient
import kotlinx.coroutines.launch

/**
 * Created by nampham on 5/10/21.
 */
class MainViewModel : ViewModel() {

    fun getNowPlaying() {
        viewModelScope.launch {
            val movieResp = RestClient.getInstance().API.listNowPlayMovies(
                language = "en-US",
                page = 1,
            )
            Log.e("TAG", movieResp.results.toString())
        }
    }

    fun getUpcoming() {
        viewModelScope.launch {
            val movieResp = RestClient.getInstance().API.listUpComingMovies(
                language = "en-US",
                page = 1,
            )
            Log.e("TAG++++ upcomming", movieResp.results.toString())
        }
    }
}