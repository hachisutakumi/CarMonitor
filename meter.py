# -*- coding: utf-8 -*-
import sys
import math
import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
import datetime
import obd



class mainWindow( QtGui.QWidget ):
	def __init__( self, parent = None ):
		super( mainWindow, self).__init__( parent )
		self.layout = QtGui.QGridLayout()

		self.meterWidget = QtGui.QGraphicsView()
		self.meterWidget = MeterView()

		self.layout.addWidget( self.meterWidget )

		self.setLayout( self.layout )

class MeterView( QtGui.QGraphicsView ):
	def __init__( self, parent = None ):
		super( MeterView, self).__init__( parent )
		#self.main_layout = QtGui.QGridLayout()

		self.setSceneRect( -150, -150, 300, 300)
		#timer
		self.timer = QtCore.QTimer( self )
		self.timer.timeout.connect( self.updateWindow )
		self.timer.start( 200 )
		#dateLabel
		self.font=QtGui.QFont() # フォント書式を生成
		self.font.setPointSize( 32 ) # フォントサイズを変更
		self.dateLabel = QtGui.QLabel( "METER" )
		self.dateLabel.setFont( self.font ) # ラベルのフォントに指定
		self.scene = Meter()
		self.setScene( self.scene )

	def updateWindow( self ):
		self.scene.update()


class Meter( QtGui.QGraphicsScene ):
	def __init__( self, parent = None ):
		super( Meter, self).__init__(  )
#なぞのじゅもん
		#self.setCacheMode( QtGui.QGraphicsView.CacheBackground )
#        self.setRenderHints( QtGui.QPainter.Antialiasing |
#            QtGui.QPainter.SmoothPixmapTransform |
#            QtGui.QPainter.TextAntialiasing
#        )
		self.__Dial = None
		self.__Value = 0.0
		self.__ValueLavel = QtGui.QGraphicsSimpleTextItem()
		self.__ValueLavelFont = QtGui.QFont( "Times", 64, QtGui.QFont.Bold)
		self.__StartAngle = 70
		self.__EndAngle = 290
		self.__MinValue = 0
		self.__MaxValue = 200
		self.__Step = 10
		self.__Name = "time"
		self.__Unit = "[sec]"
		self.__UnitLabel = QtGui.QGraphicsSimpleTextItem()
		self.__UnitLabelFont = QtGui.QFont( "Times", 32, QtGui.QFont.Bold)

		self.OBD = obd.OBD()

		#文字盤の作成
		i = 0
		while i <= self.__Step:
			shita = math.radians( ( self.__EndAngle - self.__StartAngle) / self.__Step * i + self.__StartAngle + 90)
			lineItem  = QtGui.QGraphicsLineItem(
				math.cos( shita ) * 90,
				math.sin( shita ) * 90,
				math.cos( shita ) * 100,
				math.sin( shita ) * 100
			)
			lineItem.setFlags( QtGui.QGraphicsItem.ItemIsMovable )
			pen = QtGui.QPen( QtGui.QColor( 'black' ) )
			pen.setWidth( 6 )
			lineItem.setPen( pen )
			self.addItem(lineItem)
			i = i + 1
		self.__UnitLabel.setFont( self.__UnitLabelFont )
		self.__UnitLabel.setText( self.__Unit )
		#self.addItem( self.__UnitLabel )

		#Needleの初期化
		self.__Needle  = QtGui.QGraphicsLineItem()
		self.__NeedlePen = QtGui.QPen()
		self.__NeedlePen.setWidth( 4 )
		self.__NeedlePen.setBrush( QtGui.QColor( "red" ) )
		self.__Needle.setPen( self.__NeedlePen )
		self.addItem( self.__Needle )
		self.draw()

		#ValueLabelの初期化
		self.__ValueLavel.setFont( self.__ValueLavelFont )
		self.addItem( self.__ValueLavel )

	def update( self ):
		#時間取得
		#date = datetime.datetime.today()
		#self.__Value = 1.0 * date.second

		#水温取得
		res = self.OBD.query( obd.commands.COOLANT_TEMP )
		self.__Value = res.value

		#moji
		valueString = QtCore.QString.number(self.__Value, 'g', 4)
		self.__ValueLavel.setText( valueString )

		self.draw()

	def draw( self ):
		shita = self.scalingAngle( self.__Value )
		self.__Needle.setLine(
			math.cos( shita ) * 60,
			math.sin( shita ) * 60,
			math.cos( shita ) * 100,
			math.sin( shita ) * 100
		)


	def scalingAngle( self, value ):
		if value > self.__MaxValue:
			value = self.__MaxValue
		if value < self.__MinValue:
			value = self.__MinValue
		value = value - self.__MinValue
		return math.radians( 1.0 * value * ( self.__EndAngle - self.__StartAngle ) / ( self.__MaxValue - self.__MinValue ) + self.__StartAngle + 90 )





print "start car monitor!"

if __name__ == '__main__':
	app = QtGui.QApplication( sys.argv )
	mainWidget = mainWindow()
	mainWidget.setWindowTitle('Meter')
	mainWidget.show()
	sys.exit( app.exec_() )
