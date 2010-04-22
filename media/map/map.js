var sphericalMercator = new OpenLayers.Projection("EPSG:900913");
var gps = new OpenLayers.Projection("EPSG:4326");

var map;
var worldBounds = new OpenLayers.Bounds(-20037508, -20037508, 20037508, 20037508.34);

function initMap(){
    map = new OpenLayers.Map({'div':'map',
                  projection: sphericalMercator,
                  units: 'm',
                  numZoomLevels: 18,
                  maxResolution: 156543.0339,
                  maxExtent: worldBounds});
    var layer_switcher = new OpenLayers.Control.customLayerSwitcher({div:OpenLayers.Util.getElement('layerswitcher'),
                             minimizeDiv:OpenLayers.Util.getElement('layerswitcher'),
                             maximizeDiv:OpenLayers.Util.getElement('layerswitcher'),
                             activeColor:'white'});
                             //need to pass these to switcher, to avoid ie _eventcacheID failure
    map.addControl(layer_switcher);
    
    var cloudmade = new OpenLayers.Layer.CloudMade("OpenStreetMap", {
            projection:sphericalMercator,
            key: '37409ea4915a5145b85ba77588e4cea0',
            //styleId: 1551, //farn 1 style, very clean
            styleId:2, //FineLine, faster updates
            isBaseLayer:true});
    map.addLayer(cloudmade);

    map.setCenter(new OpenLayers.LonLat(0, 0), 1);
}