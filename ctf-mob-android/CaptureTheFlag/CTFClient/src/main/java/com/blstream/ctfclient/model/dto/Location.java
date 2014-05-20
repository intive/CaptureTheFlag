package com.blstream.ctfclient.model.dto;

import com.google.android.gms.maps.model.LatLng;

/**
 * Created by mar on 28.04.14.
 */
public class Location {

    private float lat;
    private float lon;

    public Location(float lat, float lon) {
        this.lat = lat;
        this.lon = lon;
    }

    public Location(LatLng latLng) {
        this.lat = (float) latLng.latitude;
        this.lon = (float) latLng.longitude;
    }

    public float getLat() {
        return lat;
    }

    public void setLat(float lat) {
        this.lat = lat;
    }

    public float getLon() {
        return lon;
    }

    public void setLon(float lon) {
        this.lon = lon;
    }

    @Override
    public String toString() {
        return "Location{" +
                "lat=" + lat +
                ", lon=" + lon +
                '}' + toLatLng().toString();
    }

    public void addToLat(float val) {
        lat += val;
    }

    public void addToLon(float val) {
        lon += val;
    }

    public LatLng toLatLng() {
        return new LatLng(lat, lon);
    }
}
