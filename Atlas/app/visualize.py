import open3d as o3d

mesh = o3d.io.read_triangle_mesh("results/release/semseg/test_final/sample1.ply")
o3d.visualization.draw_geometries([mesh], mesh_show_wireframe=True, mesh_show_back_face=True)