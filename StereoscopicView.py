from vtk import*
layoutManager = slicer.app.layoutManager()
threeDWidget = layoutManager.threeDWidget(0)
threeDView = threeDWidget.threeDView()
renWin = threeDView.renderWindow()
rendererL = renWin.GetRenderers().GetFirstRenderer()

rendererL.SetViewport(0,0,0.5,1)
rendererL.SetBackground(0,0,0)
rendererL.GetActiveCamera().SetPosition(50,200,-100)

rendererR = vtk.vtkRenderer()
rendererR.SetViewport(0.5,0,1,1)
rendererR.SetBackground(0,0,0)
rendererR.GetActiveCamera().SetPosition(75,200,-100)
renWin.AddRenderer(rendererR)

camera0 = rendererL.GetActiveCamera()
camera1 = rendererR.GetActiveCamera()
eyedist = 50

# copy actors
actors =  rendererL.GetActors()
actors.InitTraversal()
for i in range(0, actors.GetNumberOfItems()):
  actor = actors.GetNextActor()
  if actor is not None:
    rendererR.AddActor(actor) 

volumes = rendererL.GetVolumes()
volumes.InitTraversal()
for i in range(0, volumes.GetNumberOfItems()):
  item = volumes.GetNextItem()
  if actor is not None:    
    rendererR.AddVolume(item)    

props = rendererL.GetViewProps()
props.InitTraversal()
for i in range(0, props.GetNumberOfItems()):
  prop = props.GetNextProp()
  if prop is not None:
    rendererR.AddViewProp(prop)
	
def onMouseMove(observer,eventid):
  updateCameraPositions()
  camera1.SetFocalPoint(camera0.GetFocalPoint())
  camera1.SetDistance(camera0.GetDistance())
  camera1.SetRoll(camera0.GetRoll())
  camera1.SetViewUp(camera0.GetViewUp())
  
  
def updateCameraPositions():
  pos = camera0.GetPosition()
  pos2 = [pos[0] - 65, pos[1], pos[2]]
  camera1.SetPosition(pos2)
  rendererL.ResetCameraClippingRange()
  rendererR.ResetCameraClippingRange()
  
 
 
camera0.AddObserver(vtk.vtkCommand.ModifiedEvent, onMouseMove) 

## slider to adjust spacing between eyes
slider = qt.QSlider()
slider.setOrientation(1) # horizontal slider
slider.setMinimum(0)
slider.setMaximum(500)
slider.setWindowTitle('Distance between eyes')
slider.setMinimumHeight(25)
slider.setMinimumWidth(500)
slider.valueChanged.connect(sliderChange)
slider.show()
