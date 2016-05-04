# -*- coding: utf-8 -*-
import sys
import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui

#OBDコネクタ接続時にインポート
#import obd


class mainWindow( QtGui.QWidget ):
	def __init__( self, parent = None ):
		super( mainWindow, self).__init__( parent )
		self.main_layout = QtGui.QGridLayout()
		#timer
		self.timer = QtCore.QTimer( self )
		self.timer.timeout.connect( self.updateWindow )
		self.timer.start( 200 )
		#title
		self.font=QtGui.QFont() # フォント書式を生成
		self.font.setPointSize( 32 ) # フォントサイズを変更
		self.titleText = QtGui.QLabel( "CAR MONITOR" )
		self.titleText.setFont( self.font ) # ラベルのフォントに指定
		self.main_layout.addWidget( self.titleText, 1, 1, 1, 4 )
		#coolantTemp
		self.coolantTempMeter = meterWidget()
		self.main_layout.addWidget( self.coolantTempMeter, 2, 1, 4, 4 )

		self.setLayout( self.main_layout )

	def updateWindow( self ):
		pass

class meterWidget( QtGui.QWidget ):
	def __init__( self, parent = None ):
		super( meterWidget, self).__init__( parent )
		self.name = QtGui.QLabel( "name" )
		self.value = QtGui.QLabel( "98" )
		self.unit = QtGui.QLabel( "unit" )
		#レイアウト
		self.main_layout = QtGui.QGridLayout()
		self.main_layout.addWidget( self.name, 1, 1, 1, 3)
		self.main_layout.addWidget( self.value, 2, 1, 2, 2)
		self.main_layout.addWidget( self.unit,	2, 3, 2, 3)
		self.setLayout( self.main_layout )




print "start car monitor!"

if __name__ == '__main__':
	app = QtGui.QApplication( sys.argv )
	mainWidget = mainWindow()

	mainWidget.show()
	sys.exit( app.exec_() )
