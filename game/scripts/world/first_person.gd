class_name RoomWalker
extends CharacterBody3D

var camera: Camera3D
var enabled := true
var pitch := 0.0
const SPEED := 1.85
const SENSITIVITY := 0.0023

func _ready() -> void:
	name = "RoomWalker"
	collision_layer = 2
	collision_mask = 1
	var capsule := CapsuleShape3D.new()
	capsule.radius = 0.23
	capsule.height = 1.65
	var collider := CollisionShape3D.new()
	collider.shape = capsule
	collider.position.y = 0.84
	add_child(collider)
	camera = Camera3D.new()
	camera.position.y = 1.62
	camera.fov = 62
	camera.near = 0.045
	camera.far = 70.0
	add_child(camera)
	camera.current = true

func look(relative: Vector2) -> void:
	if not enabled: return
	rotation.y -= relative.x * SENSITIVITY
	pitch = clampf(pitch-relative.y*SENSITIVITY, -1.30, 1.30)
	camera.rotation.x = pitch

func aim(target: Vector3) -> void:
	camera.look_at(target)
	var angles := camera.global_rotation
	rotation.y = angles.y
	pitch = angles.x
	camera.rotation = Vector3(pitch,0,0)

func _physics_process(delta: float) -> void:
	var axis := Vector2.ZERO
	if enabled:
		axis.x = float(Input.is_physical_key_pressed(KEY_D) or Input.is_physical_key_pressed(KEY_RIGHT)) - float(Input.is_physical_key_pressed(KEY_A) or Input.is_physical_key_pressed(KEY_Q) or Input.is_physical_key_pressed(KEY_LEFT))
		axis.y = float(Input.is_physical_key_pressed(KEY_S) or Input.is_physical_key_pressed(KEY_DOWN)) - float(Input.is_physical_key_pressed(KEY_W) or Input.is_physical_key_pressed(KEY_Z) or Input.is_physical_key_pressed(KEY_UP))
	var direction := basis * Vector3(axis.x,0,axis.y).normalized()
	velocity.x = direction.x*SPEED
	velocity.z = direction.z*SPEED
	if is_on_floor(): velocity.y = 0
	else: velocity.y -= 9.8*delta
	move_and_slide()

func target() -> String:
	var from := camera.global_position
	var to := from-camera.global_basis.z*2.25
	var query := PhysicsRayQueryParameters3D.create(from,to,1)
	var hit := get_world_3d().direct_space_state.intersect_ray(query)
	if hit.is_empty(): return ""
	var object: Node = hit.collider.get_parent()
	if object.has_meta("interaction"): return object.get_meta("interaction")
	return ""
