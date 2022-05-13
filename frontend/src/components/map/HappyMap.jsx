import React from "react";
import { MapContainer, GeoJSON } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import "./Map.css";
const HappyMap = ({ areas }) => {
  const mapStyle = {
    fillColor: "white",
    weight: 1,
    color: "black",
    fillOpacity: 1,
  };

  const h_onEachArea = (area, layer) => {
    layer.options.fillColor = area.properties.color;

    const line = "require parameters";
    const name = area.properties.ADMIN;
    const src_B = area.properties.src_B;

    if (name != null && src_B != null) {
      layer.bindPopup(`${name} ${src_B}`);
    } else {
      layer.bindPopup(`${line}`);
    }
  };

  return (
    <MapContainer style={{ height: "90vh" }} zoom={4} center={[-25, 140]}>
      <GeoJSON
        style={mapStyle}
        data={areas}
        onEachFeature={h_onEachArea}
      />
    </MapContainer>
  );
};

export default HappyMap;