import 'dart:io';
import 'package:flutter/material.dart';
import 'package:video_thumbnail/video_thumbnail.dart';
import 'package:path_provider/path_provider.dart';

class VideoThumbnailWidget extends StatefulWidget {
  final String videoPath;

  const VideoThumbnailWidget({Key? key, required this.videoPath}) : super(key: key);

  @override
  _VideoThumbnailWidgetState createState() => _VideoThumbnailWidgetState();
}

class _VideoThumbnailWidgetState extends State<VideoThumbnailWidget> {
  String? _thumbnailPath;

  @override
  void initState() {
    super.initState();
    _generateThumbnail();
  }

  Future<void> _generateThumbnail() async {
    final tempDir = await getTemporaryDirectory();
    final thumbnailPath = await VideoThumbnail.thumbnailFile(
      video: widget.videoPath,
      thumbnailPath: '${tempDir.path}/thumb.png',
      imageFormat: ImageFormat.PNG,
      maxWidth: 200,
      quality: 75,
    );

    setState(() {
      _thumbnailPath = thumbnailPath;
    });
  }

  @override
  Widget build(BuildContext context) {
    return _thumbnailPath != null
        ? Image.file(File(_thumbnailPath!))
        : CircularProgressIndicator();
  }
}
