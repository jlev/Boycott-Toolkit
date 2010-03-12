var sphericalMercator = new OpenLayers.Projection("EPSG:900913");
var gps = new OpenLayers.Projection("EPSG:4326");
var israeltm = new OpenLayers.Projection("EPSG:2039");

var map;
var worldBounds = new OpenLayers.Bounds(-20037508, -20037508, 20037508, 20037508.34);

function initMap(){
    map = new OpenLayers.Map({'div':'map',
                  projection: sphericalMercator,
                  units: 'm',
                  numZoomLevels: 18,
                  maxResolution: 156543.0339,
                  maxExtent: worldBounds});
    /*var layer_switcher = new OpenLayers.Control.customLayerSwitcher({div:OpenLayers.Util.getElement('layerswitcher'),
    //need to pass these to switcher, to avoid ie _eventcacheID failure
                                                                    minimizeDiv:OpenLayers.Util.getElement('layerswitcher'),
                                                                    maximizeDiv:OpenLayers.Util.getElement('layerswitcher'),
                                                                    activeColor:'white'});
    map.addControl(layer_switcher);
    */
    
    var cloudmade = new OpenLayers.Layer.CloudMade("OpenStreetMap", {
            projection:sphericalMercator,
            key: '37409ea4915a5145b85ba77588e4cea0',
            styleId: 1551, //farn 1 style, very clean
            isBaseLayer:true});
    map.addLayer(cloudmade);
/*    
    //the json parser, defines projections to do transform automatically on load
    json_format = new OpenLayers.Format.GeoJSON({
        internalProjection:sphericalMercator,
        externalProjection:israeltm
    });
    
    var border = new OpenLayers.Layer.Vector("Green Line", {
                                                   strategies: [new OpenLayers.Strategy.Fixed()],
                                                   protocol: new OpenLayers.Protocol.HTTP({
                                                       url: "/proxy/http://groundtruth.media.mit.edu/border.json",
                                                       format: json_format}),
                                                   projection:israeltm,
                                                   styleMap:greenlineStyleMap,
                                                   visibility:true,
                                                   infoLink:'/border/info',
                                                   loadingImg:true});
    map.addLayer(border);
    
    settlements = new OpenLayers.Layer.Vector("Settlements", {
                                                strategies: [new OpenLayers.Strategy.Fixed()],
                                                protocol: new OpenLayers.Protocol.HTTP({
                                                    url: "/proxy/http://groundtruth.media.mit.edu/settlement.json",
                                                    format: json_format}),
                                                projection:israeltm,
                                                styleMap:settlementStyleMap,
                                                visibility:true,
                                                infoLink:'/settlement/info',
                                                loadingImg:true});
    map.addLayer(settlements);
    
    palestinian = new OpenLayers.Layer.Vector("Palestinian Areas", {
                                                strategies: [new OpenLayers.Strategy.Fixed()],
                                                protocol: new OpenLayers.Protocol.HTTP({
                                                    url: "/proxy/http://groundtruth.media.mit.edu/palestinian.json",
                                                    format: json_format}),
                                                projection:israeltm,
                                                styleMap:osloAStyleMap,
                                                visibility:false,
                                                loadingImg:true});
    map.addLayer(palestinian);
    
    var barrier = new OpenLayers.Layer.Vector("Barrier", {
                                                   strategies: [new OpenLayers.Strategy.Fixed()],
                                                   protocol: new OpenLayers.Protocol.HTTP({
                                                       url: "/proxy/http://groundtruth.media.mit.edu/barrier.json",
                                                       format: json_format}),
                                                   projection:israeltm,
                                                   styleMap:barrierStyleMap,
                                                   visibility:true,
                                                   infoLink:'/barrier/info',
                                                   loadingImg:true});
    map.addLayer(barrier);
*/

    map.setCenter(new OpenLayers.LonLat(0, 0), 1);
    //map.setCenter(new OpenLayers.LonLat(3880000, 3755000), 9);
}