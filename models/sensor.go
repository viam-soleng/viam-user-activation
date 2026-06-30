// Package models implements the viam-soleng:user-activation:sensor model.
package models

import (
	"context"
	"sync"

	"go.viam.com/rdk/components/sensor"
	"go.viam.com/rdk/logging"
	"go.viam.com/rdk/resource"
)

// UserActivation is the model triple for this sensor.
var UserActivation = resource.NewModel("viam-soleng", "user-activation", "sensor")

func init() {
	resource.RegisterComponent(sensor.API, UserActivation,
		resource.Registration[sensor.Sensor, *Config]{
			Constructor: newUserActivationSensor,
		},
	)
}

// Config holds the user-configurable attributes for the sensor.
//
// activation_date is an ISO 8601 timestamp (UTC) and may be null/unset, which
// is represented as a nil pointer. delete_flag defaults to false when omitted.
type Config struct {
	ActivationDate *string `json:"activation_date,omitempty"`
	DeleteFlag     bool    `json:"delete_flag,omitempty"`
}

// Validate ensures the config is well-formed and reports dependencies. This
// sensor needs no dependencies, so it returns empty required/optional lists.
func (cfg *Config) Validate(path string) ([]string, []string, error) {
	return nil, nil, nil
}

type userActivationSensor struct {
	resource.Named
	resource.TriviallyCloseable

	logger logging.Logger

	mu             sync.Mutex
	activationDate *string
	deleteFlag     bool
}

func newUserActivationSensor(ctx context.Context, deps resource.Dependencies, conf resource.Config, logger logging.Logger) (sensor.Sensor, error) {
	s := &userActivationSensor{
		Named:  conf.ResourceName().AsNamed(),
		logger: logger,
	}
	if err := s.Reconfigure(ctx, deps, conf); err != nil {
		return nil, err
	}
	return s, nil
}

// Reconfigure dynamically updates the sensor's state when it receives a new
// config object.
func (s *userActivationSensor) Reconfigure(ctx context.Context, deps resource.Dependencies, conf resource.Config) error {
	cfg, err := resource.NativeConfig[*Config](conf)
	if err != nil {
		return err
	}

	s.mu.Lock()
	defer s.mu.Unlock()
	s.activationDate = cfg.ActivationDate
	s.deleteFlag = cfg.DeleteFlag

	s.logger.Infof("Reconfigured: activation_date=%v, delete_flag=%v", activationDateLog(s.activationDate), s.deleteFlag)
	return nil
}

// Readings returns the current activation state as sensor readings.
func (s *userActivationSensor) Readings(ctx context.Context, extra map[string]interface{}) (map[string]interface{}, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	return s.activationState(), nil
}

// DoCommand handles DoCommand requests for activation state management.
//
// Supported commands:
//   - get_activation_state: returns the current state
func (s *userActivationSensor) DoCommand(ctx context.Context, command map[string]interface{}) (map[string]interface{}, error) {
	cmd, _ := command["command"].(string)

	switch cmd {
	case "get_activation_state":
		s.logger.Debug("Getting activation state")
		s.mu.Lock()
		defer s.mu.Unlock()
		return s.activationState(), nil
	default:
		errMsg := "Unknown command: " + cmd
		s.logger.Error(errMsg)
		return map[string]interface{}{"success": false, "error": errMsg}, nil
	}
}

// activationState returns the current state as a map. Callers must hold s.mu.
func (s *userActivationSensor) activationState() map[string]interface{} {
	var activationDate interface{}
	if s.activationDate != nil {
		activationDate = *s.activationDate
	}
	return map[string]interface{}{
		"activation_date": activationDate,
		"delete_flag":     s.deleteFlag,
	}
}

// activationDateLog renders a nil pointer as "<nil>" for logging, otherwise the
// underlying string value.
func activationDateLog(d *string) interface{} {
	if d == nil {
		return nil
	}
	return *d
}
