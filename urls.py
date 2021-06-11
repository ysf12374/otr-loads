from django.urls import path,re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.http import StreamingHttpResponse

urlpatterns = [
	path('network_graph', views.network_graph, name='network_graph'),
	path('network_graph_all', views.network_graph_all, name='network_graph_all'),
	path('graph_plotly', views.graph_plotly, name='graph'),
	path('load_v_trucks', views.load_v_trucks, name='load_v_trucks'),
	path('map_arc', views.map_arc, name='map_arc'),
	path('map_heat', views.map_heat, name='map_heat'),
	path('map_time', views.map_time, name='map_time'),
	path('load_line', views.load_line, name='load_line'),
	path('just_map', views.just_map, name='just_map'),
	path('just_map_cities', views.just_map_cities, name='just_map_cities'),
	path('just_map_api', views.just_map_api, name='just_map_api'),
	path('just_map_api_2', views.just_map_api_2, name='just_map_api_2'),
	path('just_map_heat_api', views.just_map_heat_api, name='just_map_heat_api'),
	path('', views.just_map_v15, name='index'),
	path('just_map_v2', views.just_map_v2, name='just_map_v2'),
	path('just_map_v3', views.just_map_v3, name='just_map_v3'),
	path('just_map_v4', views.just_map_v4, name='just_map_v4'),
	path('just_map_v2_api', views.just_map_v2_api, name='just_map_v2_api'),
	path('just_map_v3_api', views.just_map_v3_api, name='just_map_v3_api'),
	path('just_map_v4_api', views.just_map_v4_api, name='just_map_v4_api'),
	path('just_map_v2_heat_api', views.just_map_v2_heat_api, name='just_map_v2_heat_api'),
	path('just_map_v2_circles', views.just_map_v2_circles, name='just_map_v2_circles'),
	path('just_map_v4_shipper_api', views.just_map_v4_shipper_api, name='just_map_v4_shipper_api'),
	path('just_map_v4_receiver_api', views.just_map_v4_receiver_api, name='just_map_v4_receiver_api'),
	path('just_map_v5', views.just_map_v5, name='just_map_v5'),
	path('just_map_v5_api', views.just_map_v5_api, name='just_map_v5_api'),
	path('just_map_v5_shipper_api', views.just_map_v5_shipper_api, name='just_map_v5_shipper_api'),
	path('just_map_v5_receiver_api', views.just_map_v5_receiver_api, name='just_map_v5_receiver_api'),
	path('just_map_v5_time_api', views.just_map_v5_time_api, name='just_map_v5_time_api'),
	path('just_map_v5_heat_api', views.just_map_v5_heat_api, name='just_map_v5_heat_api'),
	path('just_map_v5_time_heat_api', views.just_map_v5_time_heat_api, name='just_map_v5_time_heat_api'),
	path('just_map_get_slider_values', views.just_map_get_slider_values, name='just_map_get_slider_values'),
	path('just_map_v7', views.just_map_v7, name='just_map_v7'),
	path('just_map_v7_slider', views.just_map_v7_slider, name='just_map_v7_slider'),
	path('just_map_v8_slider', views.just_map_v8_slider, name='just_map_v8_slider'),
	path('just_map_v9', views.just_map_v9, name='just_map_v9'),
	path('just_map_v9_time_api', views.just_map_v9_time_api, name='just_map_v9_time_api'),
	path('just_map_v9_heat_chart', views.just_map_v9_heat_chart, name='just_map_v9_heat_chart'),
	path('similar_lanes', views.similar_lanes, name='similar_lanes'),
	path('just_heat_chart_v1', views.just_heat_chart_v1, name='just_heat_chart_v1'),
	path('just_heat_chart_v1_api', views.just_heat_chart_v1_api, name='just_heat_chart_v1_api'),
	path('just_map_v11_time_api', views.just_map_v11_time_api, name='just_map_v11_time_api'),
	path('just_map_v11', views.just_map_v11, name='just_map_v11'),
	path('just_map_v12', views.just_map_v12, name='just_map_v12'),
	path('just_heat_chart_v2', views.just_heat_chart_v2, name='just_heat_chart_v2'),
	path('just_map_v13', views.just_map_v13, name='just_map_v13'),
	path('just_map_v14', views.just_map_v14, name='just_map_v14'),
	path('just_map_v15', views.just_map_v15, name='just_map_v15'),
	path('just_map_hex', views.just_map_hex, name='just_map_hex'),
	path('just_map_line_graph', views.just_map_line_graph, name='just_map_line_graph'),
	path('just_map_hexagons', views.just_map_hexagons, name='just_map_hexagons'),
	path('just_map_v16', views.just_map_v16, name='just_map_v16'),
	path('just_map_carrier_api', views.just_map_carrier_api, name='just_map_carrier_api'),
	path('just_map_carrier_api2', views.just_map_carrier_api2, name='just_map_carrier_api2'),
	path('just_map_tile_id', views.just_map_tile_id, name='just_map_tile_id'),
	path('just_map_deadhead', views.just_map_deadhead, name='just_map_deadhead'),
	path('test', views.test, name='test'),
	path('just_map_loads_deadhead', views.just_map_loads_deadhead, name='just_map_loads_deadhead'),
	path('just_heat_chart_v2_api', views.just_heat_chart_v2_api, name='just_heat_chart_v2_api'),
	path('just_map_deadhead_lines', views.just_map_deadhead_lines, name='just_map_deadhead_lines'),
	path('just_map_deadhead_rig_lines', views.just_map_deadhead_rig_lines, name='just_map_deadhead_rig_lines'),
	path('just_map_heat_chart_click', views.just_map_heat_chart_click, name='just_map_heat_chart_click'),

]

# http://127.0.0.1:8000/network_graph?company%5B%5D=Allen+Lund+Company&carrier%5B%5D=Advance+Transportation+Systems+Inc&location%5B%5D=IL+BOLINGBROOK-%3EOH+VAN+BUREN
