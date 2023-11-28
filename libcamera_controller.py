import os


def help():
	print(
		"Import libcamera_controller.camera() to access libcamera apps from the terminal\n" \
		"To run a command, pass it through camera()\n" \
		"To run a command after initializing camera(), pass it through camera.run()\n" \
		"To run libcamera-still or libcamera-vid via the camera() class,\n" \
		"    Use the class methods to configure the camera options\n" \
		"    (you can also use keyword arguments)\n" \
		"    Then use run_still() or run_vid()\n" \
		"\n" \
		"Supported options:\n" \
		"    --info-text\n" \
		"    --width\n" \
		"    --height\n" \
		"    --timeout\n" \
		"    --output\n" \
		"    --post-process-file\n" \
		"    --rawfull\n" \
		"    --nopreview\n" \
		"    --fullscreen\n" \
		"    --hflip\n" \
		"    --vflip\n" \
		"    --rotation\n" \
		"    --roi\n" \
		"    --shutter\n" \
		"    --gain\n" \
		"    --exposure\n" \
		"    --ev\n" \
		"    --awb\n" \
		"    --awbgains\n" \
		"    --brightness\n" \
		"    --contrast\n" \
		"    --saturation\n" \
		"    --sharpness\n" \
		"    --framerate\n" \
		"    --denoise\n" \
		"    --lens-position\n" \
		"    --metadata\n" \
		"    --metadata-format\n" \
		"libcamera-vid specific options:\n" \
		"    --bitrate\n" \
		"    --codec\n" \
		"Find more options via the terminal with: [command] --help\n" \
	)


class camera:
	def __init__(self, *args, **kwargs):
		self.options_dict = {
			"--info-text": None,
			"--width": None,
			"--height": None,
			"--timeout": None,
			"--output": "test.mjpeg",
			"--post-process-file": None,
			"--rawfull": None,
			"--nopreview": None,
			"--preview": None,
			"--fullscreen": None,
			"--hflip": None,
			"--vflip": None,
			"--rotation": None,
			"--roi": None,
			"--shutter": None,
			"--gain": None,
			"--exposure": None,
			"--ev": None,
			"--awb": None,
			"--awbgains": None,
			"--brightness": None,
			"--contrast": None,
			"--saturation": None,
			"--sharpness": None,
			"--framerate": None,
			"--denoise": None,
			"--lens-position": None,
			"--metadata": None,
			"--metadata-format": None
			}
		self.vid_options_dict = {
			"--bitrate": None,
			"--codec": "mjpeg"
			}
		if len(args) == 1:
			if args[0][0:9] == "libcamera":
				self.run(args[0])
		if len(kwargs) > 0:
			for keyword in kwargs:
				option = "--" + keyword.replace("_", "-")
				if option == "--info-text" or keyword == "infotext":
					self.set_window_title(kwargs[keyword])
				elif option == "--nopreview" or keyword == "no_preview":
					self.set_nopreview(kwargs[keyword])
				elif option == "--preview":
					self.set_preview_position(kwargs[keyword])
				elif option in [key for key in self.options_dict]:
					if option == "--roi" or option == "--awbgains":
						self.options_dict[option] = ",".join([str(item) for item in kwargs[keyword]])
					else:
						self.options_dict[option] = kwargs[keyword]
				elif keyword in [key for key in self.vid_options_dict]:
					self.vid_options_dict[option] = kwargs[keyword]
				elif keyword == "t":
					self.options_dict["--timeout"] = kwargs[keyword]
				elif keyword == "o":
					self.options_dict["--output"] = kwargs[keyword]
				elif keyword == "n":
					self.set_nopreview(kwargs[keyword])
				elif keyword == "p":
					self.set_preview_position(kwargs[keyword])
				elif keyword == "f":
					self.options_dict["--fullscreen"] = kwargs[keyword]
				elif keyword == "b":
					self.vid_options_dict["--bitrate"] = (kwargs[keyword])
	
	
	def show_options(self):
		for key in self.options_dict:
			print(f"{key}: {self.options_dict[key]}")
		for key in self.vid_options_dict:
			print(f"{key}: {self.vid_options_dict[key]}")
	
	
	def reset_options(self):
		for key in self.options_dict:
			self.options_dict[key] = None
		for key in self.vid_options_dict:
			self.vid_options_dict[key] = None
	
	
	def set_window_title(self, info_text):
		# --info-text
		# available values:
		#     %frame	(frame number)
		#     %fps	(frame rate)
		#     %exp	(shutter speed)
		#     %ag	(analog gain)
		#     %dg	(digital gain)
		#     %rg	(red color gain)
		#     %bg	(blue color gain)
		#     %focus	(focus FoM value)
		#     %aelock	(AE lock status)
		#     %lp	(lens position, if known)
		#     %afstate	(auto focus state, if supported)
		if info_text == None:
			self.options_dict["--info-text"] = None
		elif isinstance(info_text, str):
			self.options_dict["--info-text"] = info_text
		elif all(isinstance(text, str) for text in info_text):
			self.options_dict["--info-text"] = " ".join(info_text)
		else:
			print("Expected 'str', list of 'str', or None\n")
	
	
	def set_image_resolution(self, width, height):
		# --width
		# --height
		# 0 = use default
		self.options_dict["--width"] = width
		self.options_dict["--height"] = height
	
	
	def set_display_duration(self, display_duration):
		# --timeout, -t
		# if no units are provided, defaults to ms
		self.options_dict["--timeout"] = display_duration
	
	
	def set_file_name(self, file_name):
		# --output, -o
		self.options_dict["--output"] = file_name
	
	
	def set_post_processing_file_name(self, file_name):
		# --post-process-file
		self.options_dict["--post-process-file"] = file_name
	
	
	def force_raw_frames(self, rawfull=1):
		# --rawfull
		self.options_dict["--rawfull"] = rawfull
	
	
	def set_nopreview(self, nopreview=1):
		# --nopreview, -n
		if str(nopreview) == "1" or str(nopreview) == "True":
			self.options_dict["--preview"] = None
			self.options_dict["--nopreview"] = "1"
		else:
			self.options_dict["--nopreview"] = None
	
	def set_preview_position(self, x, y, width, height):
		# --preview, -p (given as x,y,width,height)
		self.options_dict["--nopreview"] = None
		self.options_dict["--preview"] = str(x) + "," + str(y) + "," + str(width) + "," + str(height)
	
	def use_fullscreen(self, fullscreen=1):
		# --fullscreen, -f
		self.options_dict["--fullscreen"] = fullscreen
	
	
	def horizontal_flip(self, hflip=1):
		# --hflip
		self.options_dict["--hflip"] = hflip
	
	
	def vertical_flip(self, vflip=1):
		# --vflip
		self.options_dict["--vflip"] = vflip
	
	
	def set_rotation_degrees(self, rotation):
		# --rotation
		self.options_dict["--rotation"] = rotation
	
	
	def set_digital_zoom(self, roi1, roi2, roi3, roi4):
		# --roi
		self.options_dict["--roi"] = str(roi1) + "," + str(roi2) + "," + str(roi3) + "," + str(roi4)
	
	
	def set_no_digital_zoom(self, set_none):
		if set_none or set_none == None:
			self.options_dict["--roi"] = None
	
	
	def set_shutter_speed(self, shutter_speed):
		# --shutter
		self.options_dict["--shutter"] = shutter_speed
	
	
	def set_gain(self, gain):
		# --gain
		self.options_dict["--gain"] = gain
	
	
	def set_exposure(self, exposure):
		# --exposure
		self.options_dict["--exposure"] = exposure
	
	
	def set_ev_exposure_compensation(self, ev):
		# --ev
		# 0 = no change
		self.options_dict["--ev"] = ev
	
	
	def set_auto_white_balance_mode(self, awb):
		# --awb
		# auto, incandescent, tungsten, fluorescent, indoor, daylight
		self.options_dict["--awb"] = awb
	
	
	def set_auto_white_balance_gains(self, red_gain, blue_gain):
		# --awbgains
		# disables the automatic AWB algorithm
		self.options_dict["--awbgains"] = str(red_gain) + "," + str(blue_gain)
	
	
	def set_brightness(self, brightness):
		# --brightness
		# range: -1.0 to 1.0
		self.options_dict["--brightness"] = brightness
	
	
	def set_contrast(self, contrast):
		# --contrast
		# 1.0 = normal contrast
		self.options_dict["--contrast"] = contrast
	
	
	def set_saturation(self, saturation):
		# --saturation
		# 1.0 = normal saturation
		# 0.0 = greyscale
		self.options_dict["--saturation"] = saturation
	
	
	def set_sharpness(self, sharpness):
		# --sharpness
		# 1.0 = normal sharpening
		self.options_dict["--sharpness"] = sharpness
	
	
	def set_frame_rate(self, frame_rate=10):
		# --framerate
		self.options_dict["--framerate"] = frame_rate
	
	
	def set_denoise_mode(self, denoise):
		# --denoise
		# auto, off, cdn_off, cdn_fast, cdn_hq
		self.options_dict["--denoise"] = denoise
	
	
	def set_lens_position(self, lens_position):
		# --lens-position
		# 0 = infinity
		# "default" = hyperfocal distance
		self.options_dict["--lens-position"] = lens_position
	
	
	def set_metadata(self, metadata):
		# --metadata
		self.options_dict["--metadata"] = metadata
	
	
	def set_metadata_format(self, metadata_format):
		# --metadata-format
		# requires --metadata
		self.options_dict["--metadata-format"] = metadata_format
	
	
	def set_video_bitrate(self, bitrate):
		# --bitrate, -b
		# if no units are provided, defaults to bits/second
		# video option only
		self.vid_options_dict["--bitrate"] = bitrate
	
	
	def set_video_codec(self, codec="mjpeg"):
		# --codec
		# h264, libav, mjpeg, yuv420
		# video option only
		self.vid_options_dict["--codec"] = codec
	
	
	def run_still(self):
		command = "libcamera-still"
		for key in self.options_dict:
			value = self.options_dict[key]
			if value != None:
				command += " " + key + " " + str(value)
		print(command)
		# os.system(command)
	
	
	def run_vid(self):
		command = "libcamera-vid"
		for key in self.options_dict:
			value = self.options_dict[key]
			if value != None:
				command += " " + key + " " + str(value)
		for key in self.vid_options_dict:
			value = self.vid_options_dict[key]
			if value != None:
				command += " " + key + " " + str(value)
		os.system(command)
	
	
	def run(self, command):
		os.system(command)


