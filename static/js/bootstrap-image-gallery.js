    1
    2
    3
    4
    5
    6
    7
    8
    9
    10
    11
    12
    13
    14
    15
    16
    17
    18
    19
    20
    21
    22
    23
    24
    25
    26
    27
    28
    29
    30
    31
    32
    33
    34
    35
    36
    37
    38
    39
    40
    41
    42
    43
    44
    45
    46
    47
    48
    49
    50
    51
    52
    53
    54
    55
    56
    57
    58
    59
    60
    61
    62
    63
    64
    65
    66
    67
    68
    69
    70
    71
    72
    73
    74
    75
    76
    77
    78
    79
    80
    81
    82
    83
    84
    85
    86
    87
    88
    89
    90
    91
    92
    93
    94
    95
    96
    97
    98
    99
    100
    101
    102
    103
    104
    105
    106
    107
    108
    109
    110
    111
    112
    113
    114
    115
    116
    117
    118
    119
    120
    121
    122
    123
    124
    125
    126
    127
    128
    129
    130
    131
    132
    133
    134
    135
    136
    137
    138
    139
    140
    141
    142
    143
    144
    145
    146
    147
    148
    149
    150
    151
    152
    153
    154
    155
    156
    157
    158
    159
    160
    161
    162
    163
    164
    165
    166
    167
    168
    169
    170
    171
    172
    173
    174
    175
    176
    177
    178
    179
    180
    181
    182
    183
    184
    185
    186
    187
    188
    189
    190
    191
    192
    193
    194
    195
    196
    197
    198
    199
    200
    201
    202
    203
    204
    205
    206
    207
    208
    209
    210
    211
    212
    213
    214
    215
    216
    217
    218
    219
    220
    221
    222
    223
    224
    225
    226
    227
    228
    229
    230
    231
    232
    233
    234
    235
    236
    237
    238
    239
    240
    241
    242
    243
    244
    245
    246
    247
    248
    249
    250
    251
    252
    253
    254
    255
    256
    257
    258
    259
    260
    261
    262
    263
    264
    265
    266
    267
    268
    269
    270
    271
    272
    273
    274
    275
    276
    277
    278
    279
    280
    281
    282
    283
    284
    285
    286
    287
    288
    289
    290
    291
    292
    293
    294
    295
    296
    297
    298
    299
    300
    301
    302
    303
    304
    305
    306
    307
    308
    309
    310
    311
    312
    313
    314
    315
    316
    317
    318
    319
    320
    321
    322
    323
    324
    325
    326
    327
    328
    329
    330
    331
    332
    333
    334
    335
    336
    337
    338
    339
    340
    341
    342
    343
    344
    345
    346
    347
    348
    349
    350
    351
    352
    353
    354
    355
    356
    357
    358
    359
    360
    361
    362
    363
    364
    365
    366
    367
    368
    369
    370
    371
    372
    373
    374
    375
    376
    377
    378
    379
    380
    381
    382
    383
    384
    385
    386
    387
    388
    389
    390
    391
    392
    393
    394
    395
    396
    397
    398
    399
    400
    401
    402
    403
    404
    405
    406
    407
    408
    409
    410
    411
    412
    413
    414
    415
    416
    417
    418
    419
    420
    421
    422
    423
    424
    425
    426
    427
    428
    429
    430
    431
    432
    433
    434
    435
    436
    437
    438
    439
    440
    441
    442
    443
    444
    445
    446
    447
    448
    449
    450
    451
    452
    453
    454
    455
    456
    457
    458
    459
    460
    461
    462
    463
    464
    465
    466
    467
    468
    469
    470
    471
    472
    473
    474
    475
    476
    477
    478
    479
    480
    481
    482
    483
    484
    485
    486
    487
    488
    489
    490
    491
    492
    493
    494
    495
    496
    497
    498
    499
    500
    501
    502
    503
    504
    505
    506
    507
    508
    509
    510
    511
    512
    513
    514
    515
    516
    517
    518
    519
    520
    521
    522
    523
    524
    525
    526
    527
    528
    529
    530
    531
    532
    533
    534
    535
    536
    537
    538
    539
    540
    541
    542
    543
    544
    545
    546
    547
    548
    549
    550
    551
    552
    553
    554
    555
    556
    557
    558
    559
    560
    561
    562
    563
    564
    565
    566
    567
    568
    569
    570
    571

(function (e) {
    "use strict";
    var t = function (e, i, a) {
        var n, r, o = document.createElement("img");
        if (o.onerror = i, o.onload = function () {
            !r || a && a.noRevoke || t.revokeObjectURL(r), i && i(t.scale(o, a))
        }, t.isInstanceOf("Blob", e) || t.isInstanceOf("File", e)) n = r = t.createObjectURL(e), o._type = e.type;
        else {
            if ("string" != typeof e) return !1;
            n = e, a && a.crossOrigin && (o.crossOrigin = a.crossOrigin)
        }
        return n ? (o.src = n, o) : t.readFile(e, function (e) {
            var t = e.target;
            t && t.result ? o.src = t.result : i && i(e)
        })
    }, i = window.createObjectURL && window || window.URL && URL.revokeObjectURL && URL || window.webkitURL && webkitURL;
    t.isInstanceOf = function (e, t) {
        return Object.prototype.toString.call(t) === "[object " + e + "]"
    }, t.transformCoordinates = function (e, t) {
        var i = e.getContext("2d"),
            a = e.width,
            n = e.height;
        switch (t > 4 && (e.width = n, e.height = a), t) {
            case 2:
                i.translate(a, 0), i.scale(-1, 1);
                break;
            case 3:
                i.translate(a, n), i.rotate(Math.PI);
                break;
            case 4:
                i.translate(0, n), i.scale(1, -1);
                break;
            case 5:
                i.rotate(.5 * Math.PI), i.scale(1, -1);
                break;
            case 6:
                i.rotate(.5 * Math.PI), i.translate(0, -n);
                break;
            case 7:
                i.rotate(.5 * Math.PI), i.translate(a, -n), i.scale(-1, 1);
                break;
            case 8:
                i.rotate(-.5 * Math.PI), i.translate(-a, 0)
        }
    }, t.renderImageToCanvas = function (e, t, i, a, n, r, o, s, d, l) {
        return e.getContext("2d").drawImage(t, i, a, n, r, o, s, d, l), e
    }, t.scale = function (e, i) {
        i = i || {};
        var a, n, r, o, s, d, l, c = document.createElement("canvas"),
            u = e.getContext || (i.canvas || i.crop || i.orientation) && c.getContext,
            g = e.width,
            f = e.height,
            h = g,
            m = f,
            p = 0,
            S = 0,
            x = 0,
            y = 0;
        return u && i.orientation > 4 ? (a = i.maxHeight, n = i.maxWidth, r = i.minHeight, o = i.minWidth) : (a = i.maxWidth, n = i.maxHeight, r = i.minWidth, o = i.minHeight), u && a && n && i.crop ? (s = a, d = n, a / n > g / f ? (m = n * g / a, S = (f - m) / 2) : (h = a * f / n, p = (g - h) / 2)) : (s = g, d = f, l = Math.max((r || s) / s, (o || d) / d), l > 1 && (s = Math.ceil(s * l), d = Math.ceil(d * l)), l = Math.min((a || s) / s, (n || d) / d), 1 > l && (s = Math.ceil(s * l), d = Math.ceil(d * l))), u ? (c.width = s, c.height = d, t.transformCoordinates(c, i.orientation), t.renderImageToCanvas(c, e, p, S, h, m, x, y, s, d)) : (e.width = s, e.height = d, e)
    }, t.createObjectURL = function (e) {
        return i ? i.createObjectURL(e) : !1
    }, t.revokeObjectURL = function (e) {
        return i ? i.revokeObjectURL(e) : !1
    }, t.readFile = function (e, t, i) {
        if (window.FileReader) {
            var a = new FileReader;
            if (a.onload = a.onerror = t, i = i || "readAsDataURL", a[i]) return a[i](e), a
        }
        return !1
    }, "function" == typeof define && define.amd ? define(function () {
        return t
    }) : e.loadImage = t
})(this),
function (e) {
    "use strict";
    "function" == typeof define && define.amd ? define(["load-image"], e) : e(window.loadImage)
}(function (e) {
    "use strict";
    if (window.navigator && window.navigator.platform && /iP(hone|od|ad)/.test(window.navigator.platform)) {
        var t = e.renderImageToCanvas;
        e.detectSubsampling = function (e) {
            var t, i;
            return e.width * e.height > 1048576 ? (t = document.createElement("canvas"), t.width = t.height = 1, i = t.getContext("2d"), i.drawImage(e, -e.width + 1, 0), 0 === i.getImageData(0, 0, 1, 1).data[3]) : !1
        }, e.detectVerticalSquash = function (e, t) {
            var i, a, n, r, o, s = document.createElement("canvas"),
                d = s.getContext("2d");
            for (s.width = 1, s.height = t, d.drawImage(e, 0, 0), i = d.getImageData(0, 0, 1, t).data, a = 0, n = t, r = t; r > a;) o = i[4 * (r - 1) + 3], 0 === o ? n = r : a = r, r = n + a >> 1;
            return r / t || 1
        }, e.renderImageToCanvas = function (i, a, n, r, o, s, d, l, c, u) {
            if ("image/jpeg" === a._type) {
                var g, f, h, m, p = i.getContext("2d"),
                    S = document.createElement("canvas"),
                    x = 1024,
                    y = S.getContext("2d");
                if (S.width = x, S.height = x, p.save(), g = e.detectSubsampling(a), g && (o /= 2, s /= 2), f = e.detectVerticalSquash(a, s), g && 1 !== f) {
                    for (c = Math.ceil(x * c / o), u = Math.ceil(x * u / s / f), l = 0, m = 0; s > m;) {
                        for (d = 0, h = 0; o > h;) y.clearRect(0, 0, x, x), y.drawImage(a, n, r, o, s, -h, -m, o, s), p.drawImage(S, 0, 0, x, x, d, l, c, u), h += x, d += c;
                        m += x, l += u
                    }
                    return p.restore(), i
                }
            }
            return t(i, a, n, r, o, s, d, l, c, u)
        }
    }
}),
function (e) {
    "use strict";
    "function" == typeof define && define.amd ? define(["load-image"], e) : e(window.loadImage)
}(function (e) {
    "use strict";
    var t = window.Blob && (Blob.prototype.slice || Blob.prototype.webkitSlice || Blob.prototype.mozSlice);
    e.blobSlice = t && function () {
        var e = this.slice || this.webkitSlice || this.mozSlice;
        return e.apply(this, arguments)
    }, e.metaDataParsers = {
        jpeg: {
            65505: []
        }
    }, e.parseMetaData = function (t, i, a) {
        a = a || {};
        var n = this,
            r = a.maxMetaDataSize || 262144,
            o = {}, s = !(window.DataView && t && t.size >= 12 && "image/jpeg" === t.type && e.blobSlice);
        (s || !e.readFile(e.blobSlice.call(t, 0, r), function (t) {
            var r, s, d, l, c = t.target.result,
                u = new DataView(c),
                g = 2,
                f = u.byteLength - 4,
                h = g;
            if (65496 === u.getUint16(0)) {
                for (; f > g && (r = u.getUint16(g), r >= 65504 && 65519 >= r || 65534 === r);) {
                    if (s = u.getUint16(g + 2) + 2, g + s > u.byteLength) {
                        console.log("Invalid meta data: Invalid segment size.");
                        break
                    }
                    if (d = e.metaDataParsers.jpeg[r]) for (l = 0; d.length > l; l += 1) d[l].call(n, u, g, s, o, a);
                    g += s, h = g
                }!a.disableImageHead && h > 6 && (o.imageHead = c.slice ? c.slice(0, h) : new Uint8Array(c).subarray(0, h))
            } else console.log("Invalid JPEG file: Missing JPEG marker.");
            i(o)
        }, "readAsArrayBuffer")) && i(o)
    }
}),
function (e) {
    "use strict";
    "function" == typeof define && define.amd ? define(["load-image", "load-image-meta"], e) : e(window.loadImage)
}(function (e) {
    "use strict";
    e.ExifMap = function () {
        return this
    }, e.ExifMap.prototype.map = {
        Orientation: 274
    }, e.ExifMap.prototype.get = function (e) {
        return this[e] || this[this.map[e]]
    }, e.getExifThumbnail = function (e, t, i) {
        var a, n, r;
        if (!i || t + i > e.byteLength) return console.log("Invalid Exif data: Invalid thumbnail data."), void 0;
        for (a = [], n = 0; i > n; n += 1) r = e.getUint8(t + n), a.push((16 > r ? "0" : "") + r.toString(16));
        return "data:image/jpeg,%" + a.join("%")
    }, e.exifTagTypes = {
        1: {
            getValue: function (e, t) {
                return e.getUint8(t)
            },
            size: 1
        },
        2: {
            getValue: function (e, t) {
                return String.fromCharCode(e.getUint8(t))
            },
            size: 1,
            ascii: !0
        },
        3: {
            getValue: function (e, t, i) {
                return e.getUint16(t, i)
            },
            size: 2
        },
        4: {
            getValue: function (e, t, i) {
                return e.getUint32(t, i)
            },
            size: 4
        },
        5: {
            getValue: function (e, t, i) {
                return e.getUint32(t, i) / e.getUint32(t + 4, i)
            },
            size: 8
        },
        9: {
            getValue: function (e, t, i) {
                return e.getInt32(t, i)
            },
            size: 4
        },
        10: {
            getValue: function (e, t, i) {
                return e.getInt32(t, i) / e.getInt32(t + 4, i)
            },
            size: 8
        }
    }, e.exifTagTypes[7] = e.exifTagTypes[1], e.getExifValue = function (t, i, a, n, r, o) {
        var s, d, l, c, u, g, f = e.exifTagTypes[n];
        if (!f) return console.log("Invalid Exif data: Invalid tag type."), void 0;
        if (s = f.size * r, d = s > 4 ? i + t.getUint32(a + 8, o) : a + 8, d + s > t.byteLength) return console.log("Invalid Exif data: Invalid data offset."), void 0;
        if (1 === r) return f.getValue(t, d, o);
        for (l = [], c = 0; r > c; c += 1) l[c] = f.getValue(t, d + c * f.size, o);
        if (f.ascii) {
            for (u = "", c = 0; l.length > c && (g = l[c], "\0" !== g); c += 1) u += g;
            return u
        }
        return l
    }, e.parseExifTag = function (t, i, a, n, r) {
        var o = t.getUint16(a, n);
        r.exif[o] = e.getExifValue(t, i, a, t.getUint16(a + 2, n), t.getUint32(a + 4, n), n)
    }, e.parseExifTags = function (e, t, i, a, n) {
        var r, o, s;
        if (i + 6 > e.byteLength) return console.log("Invalid Exif data: Invalid directory offset."), void 0;
        if (r = e.getUint16(i, a), o = i + 2 + 12 * r, o + 4 > e.byteLength) return console.log("Invalid Exif data: Invalid directory size."), void 0;
        for (s = 0; r > s; s += 1) this.parseExifTag(e, t, i + 2 + 12 * s, a, n);
        return e.getUint32(o, a)
    }, e.parseExifData = function (t, i, a, n, r) {
        if (!r.disableExif) {
            var o, s, d, l = i + 10;
            if (1165519206 === t.getUint32(i + 4)) {
                if (l + 8 > t.byteLength) return console.log("Invalid Exif data: Invalid segment size."), void 0;
                if (0 !== t.getUint16(i + 8)) return console.log("Invalid Exif data: Missing byte alignment offset."), void 0;
                switch (t.getUint16(l)) {
                    case 18761:
                        o = !0;
                        break;
                    case 19789:
                        o = !1;
                        break;
                    default:
                        return console.log("Invalid Exif data: Invalid byte alignment marker."), void 0
                }
                if (42 !== t.getUint16(l + 2, o)) return console.log("Invalid Exif data: Missing TIFF marker."), void 0;
                s = t.getUint32(l + 4, o), n.exif = new e.ExifMap, s = e.parseExifTags(t, l, l + s, o, n), s && !r.disableExifThumbnail && (d = {
                    exif: {}
                }, s = e.parseExifTags(t, l, l + s, o, d), d.exif[513] && (n.exif.Thumbnail = e.getExifThumbnail(t, l + d.exif[513], d.exif[514]))), n.exif[34665] && !r.disableExifSub && e.parseExifTags(t, l, l + n.exif[34665], o, n), n.exif[34853] && !r.disableExifGps && e.parseExifTags(t, l, l + n.exif[34853], o, n)
            }
        }
    }, e.metaDataParsers.jpeg[65505].push(e.parseExifData)
}),
function (e) {
    "use strict";
    "function" == typeof define && define.amd ? define(["load-image", "load-image-exif"], e) : e(window.loadImage)
}(function (e) {
    "use strict";
    var t, i, a;
    e.ExifMap.prototype.tags = {
        256: "ImageWidth",
        257: "ImageHeight",
        34665: "ExifIFDPointer",
        34853: "GPSInfoIFDPointer",
        40965: "InteroperabilityIFDPointer",
        258: "BitsPerSample",
        259: "Compression",
        262: "PhotometricInterpretation",
        274: "Orientation",
        277: "SamplesPerPixel",
        284: "PlanarConfiguration",
        530: "YCbCrSubSampling",
        531: "YCbCrPositioning",
        282: "XResolution",
        283: "YResolution",
        296: "ResolutionUnit",
        273: "StripOffsets",
        278: "RowsPerStrip",
        279: "StripByteCounts",
        513: "JPEGInterchangeFormat",
        514: "JPEGInterchangeFormatLength",
        301: "TransferFunction",
        318: "WhitePoint",
        319: "PrimaryChromaticities",
        529: "YCbCrCoefficients",
        532: "ReferenceBlackWhite",
        306: "DateTime",
        270: "ImageDescription",
        271: "Make",
        272: "Model",
        305: "Software",
        315: "Artist",
        33432: "Copyright",
        36864: "ExifVersion",
        40960: "FlashpixVersion",
        40961: "ColorSpace",
        40962: "PixelXDimension",
        40963: "PixelYDimension",
        42240: "Gamma",
        37121: "ComponentsConfiguration",
        37122: "CompressedBitsPerPixel",
        37500: "MakerNote",
        37510: "UserComment",
        40964: "RelatedSoundFile",
        36867: "DateTimeOriginal",
        36868: "DateTimeDigitized",
        37520: "SubSecTime",
        37521: "SubSecTimeOriginal",
        37522: "SubSecTimeDigitized",
        33434: "ExposureTime",
        33437: "FNumber",
        34850: "ExposureProgram",
        34852: "SpectralSensitivity",
        34855: "PhotographicSensitivity",
        34856: "OECF",
        34864: "SensitivityType",
        34865: "StandardOutputSensitivity",
        34866: "RecommendedExposureIndex",
        34867: "ISOSpeed",
        34868: "ISOSpeedLatitudeyyy",
        34869: "ISOSpeedLatitudezzz",
        37377: "ShutterSpeedValue",
        37378: "ApertureValue",
        37379: "BrightnessValue",
        37380: "ExposureBias",
        37381: "MaxApertureValue",
        37382: "SubjectDistance",
        37383: "MeteringMode",
        37384: "LightSource",
        37385: "Flash",
        37396: "SubjectArea",
        37386: "FocalLength",
        41483: "FlashEnergy",
        41484: "SpatialFrequencyResponse",
        41486: "FocalPlaneXResolution",
        41487: "FocalPlaneYResolution",
        41488: "FocalPlaneResolutionUnit",
        41492: "SubjectLocation",
        41493: "ExposureIndex",
        41495: "SensingMethod",
        41728: "FileSource",
        41729: "SceneType",
        41730: "CFAPattern",
        41985: "CustomRendered",
        41986: "ExposureMode",
        41987: "WhiteBalance",
        41988: "DigitalZoomRatio",
        41989: "FocalLengthIn35mmFilm",
        41990: "SceneCaptureType",
        41991: "GainControl",
        41992: "Contrast",
        41993: "Saturation",
        41994: "Sharpness",
        41995: "DeviceSettingDescription",
        41996: "SubjectDistanceRange",
        42016: "ImageUniqueID",
        42032: "CameraOwnerName",
        42033: "BodySerialNumber",
        42034: "LensSpecification",
        42035: "LensMake",
        42036: "LensModel",
        42037: "LensSerialNumber",
        0: "GPSVersionID",
        1: "GPSLatitudeRef",
        2: "GPSLatitude",
        3: "GPSLongitudeRef",
        4: "GPSLongitude",
        5: "GPSAltitudeRef",
        6: "GPSAltitude",
        7: "GPSTimeStamp",
        8: "GPSSatellites",
        9: "GPSStatus",
        10: "GPSMeasureMode",
        11: "GPSDOP",
        12: "GPSSpeedRef",
        13: "GPSSpeed",
        14: "GPSTrackRef",
        15: "GPSTrack",
        16: "GPSImgDirectionRef",
        17: "GPSImgDirection",
        18: "GPSMapDatum",
        19: "GPSDestLatitudeRef",
        20: "GPSDestLatitude",
        21: "GPSDestLongitudeRef",
        22: "GPSDestLongitude",
        23: "GPSDestBearingRef",
        24: "GPSDestBearing",
        25: "GPSDestDistanceRef",
        26: "GPSDestDistance",
        27: "GPSProcessingMethod",
        28: "GPSAreaInformation",
        29: "GPSDateStamp",
        30: "GPSDifferential",
        31: "GPSHPositioningError"
    }, e.ExifMap.prototype.stringValues = {
        ExposureProgram: {
            0: "Undefined",
            1: "Manual",
            2: "Normal program",
            3: "Aperture priority",
            4: "Shutter priority",
            5: "Creative program",
            6: "Action program",
            7: "Portrait mode",
            8: "Landscape mode"
        },
        MeteringMode: {
            0: "Unknown",
            1: "Average",
            2: "CenterWeightedAverage",
            3: "Spot",
            4: "MultiSpot",
            5: "Pattern",
            6: "Partial",
            255: "Other"
        },
        LightSource: {
            0: "Unknown",
            1: "Daylight",
            2: "Fluorescent",
            3: "Tungsten (incandescent light)",
            4: "Flash",
            9: "Fine weather",
            10: "Cloudy weather",
            11: "Shade",
            12: "Daylight fluorescent (D 5700 - 7100K)",
            13: "Day white fluorescent (N 4600 - 5400K)",
            14: "Cool white fluorescent (W 3900 - 4500K)",
            15: "White fluorescent (WW 3200 - 3700K)",
            17: "Standard light A",
            18: "Standard light B",
            19: "Standard light C",
            20: "D55",
            21: "D65",
            22: "D75",
            23: "D50",
            24: "ISO studio tungsten",
            255: "Other"
        },
        Flash: {
            0: "Flash did not fire",
            1: "Flash fired",
            5: "Strobe return light not detected",
            7: "Strobe return light detected",
            9: "Flash fired, compulsory flash mode",
            13: "Flash fired, compulsory flash mode, return light not detected",
            15: "Flash fired, compulsory flash mode, return light detected",
            16: "Flash did not fire, compulsory flash mode",
            24: "Flash did not fire, auto mode",
            25: "Flash fired, auto mode",
            29: "Flash fired, auto mode, return light not detected",
            31: "Flash fired, auto mode, return light detected",
            32: "No flash function",
            65: "Flash fired, red-eye reduction mode",
            69: "Flash fired, red-eye reduction mode, return light not detected",
            71: "Flash fired, red-eye reduction mode, return light detected",
            73: "Flash fired, compulsory flash mode, red-eye reduction mode",
            77: "Flash fired, compulsory flash mode, red-eye reduction mode, return light not detected",
            79: "Flash fired, compulsory flash mode, red-eye reduction mode, return light detected",
            89: "Flash fired, auto mode, red-eye reduction mode",
            93: "Flash fired, auto mode, return light not detected, red-eye reduction mode",
            95: "Flash fired, auto mode, return light detected, red-eye reduction mode"
        },
        SensingMethod: {
            1: "Undefined",
            2: "One-chip color area sensor",
            3: "Two-chip color area sensor",
            4: "Three-chip color area sensor",
            5: "Color sequential area sensor",
            7: "Trilinear sensor",
            8: "Color sequential linear sensor"
        },
        SceneCaptureType: {
            0: "Standard",
            1: "Landscape",
            2: "Portrait",
            3: "Night scene"
        },
        SceneType: {
            1: "Directly photographed"
        },
        CustomRendered: {
            0: "Normal process",
            1: "Custom process"
        },
        WhiteBalance: {
            0: "Auto white balance",
            1: "Manual white balance"
        },
        GainControl: {
            0: "None",
            1: "Low gain up",
            2: "High gain up",
            3: "Low gain down",
            4: "High gain down"
        },
        Contrast: {
            0: "Normal",
            1: "Soft",
            2: "Hard"
        },
        Saturation: {
            0: "Normal",
            1: "Low saturation",
            2: "High saturation"
        },
        Sharpness: {
            0: "Normal",
            1: "Soft",
            2: "Hard"
        },
        SubjectDistanceRange: {
            0: "Unknown",
            1: "Macro",
            2: "Close view",
            3: "Distant view"
        },
        FileSource: {
            3: "DSC"
        },
        ComponentsConfiguration: {
            0: "",
            1: "Y",
            2: "Cb",
            3: "Cr",
            4: "R",
            5: "G",
            6: "B"
        },
        Orientation: {
            1: "top-left",
            2: "top-right",
            3: "bottom-right",
            4: "bottom-left",
            5: "left-top",
            6: "right-top",
            7: "right-bottom",
            8: "left-bottom"
        }
    }, e.ExifMap.prototype.getText = function (e) {
        var t = this.get(e);
        switch (e) {
            case "LightSource":
            case "Flash":
            case "MeteringMode":
            case "ExposureProgram":
            case "SensingMethod":
            case "SceneCaptureType":
            case "SceneType":
            case "CustomRendered":
            case "WhiteBalance":
            case "GainControl":
            case "Contrast":
            case "Saturation":
            case "Sharpness":
            case "SubjectDistanceRange":
            case "FileSource":
            case "Orientation":
                return this.stringValues[e][t];
            case "ExifVersion":
            case "FlashpixVersion":
                return String.fromCharCode(t[0], t[1], t[2], t[3]);
            case "ComponentsConfiguration":
                return this.stringValues[e][t[0]] + this.stringValues[e][t[1]] + this.stringValues[e][t[2]] + this.stringValues[e][t[3]];
            case "GPSVersionID":
                return t[0] + "." + t[1] + "." + t[2] + "." + t[3]
        }
        return t + ""
    }, t = e.ExifMap.prototype.tags, i = e.ExifMap.prototype.map;
    for (a in t) t.hasOwnProperty(a) && (i[t[a]] = a);
    e.ExifMap.prototype.getAll = function () {
        var e, i, a = {};
        for (e in this) this.hasOwnProperty(e) && (i = t[e], i && (a[i] = this.getText(i)));
        return a
    }
});
