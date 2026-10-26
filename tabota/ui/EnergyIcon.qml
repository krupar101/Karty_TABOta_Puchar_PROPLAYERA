import QtQuick

// Vector geometry: independent of system fonts and emoji rendering in Linux bundles.
Canvas {
    property color color: Theme.gold
    width: 16; height: 20
    onColorChanged: requestPaint()
    onPaint: {
        const ctx = getContext("2d")
        ctx.reset()
        ctx.fillStyle = color
        ctx.beginPath()
        ctx.moveTo(width * .58, 0)
        ctx.lineTo(width * .08, height * .57)
        ctx.lineTo(width * .44, height * .57)
        ctx.lineTo(width * .30, height)
        ctx.lineTo(width * .93, height * .38)
        ctx.lineTo(width * .57, height * .38)
        ctx.closePath()
        ctx.fill()
    }
}
