# User Activation Module

A Viam `sensor` component for user activation metadata in Viam.

## Model viam-soleng:user-activation:sensor

This model implements the `rdk:component:sensor` API by provinf read access to activation metadata stored via attributes. It's designed to work with external systems (mobile apps, etc.) that update the configuration via API clients.

### Configuration
The following attribute template can be used to configure this model:

```json
{
"activation_date": <timestamp>,
"delete_flag": <boolean>
}
```

#### Attributes

The following attributes are available for this model:

| Name          | Type   | Inclusion | Description                |
|---------------|--------|-----------|----------------------------|
| `activation_date` | string or null  | Optional  | ISO 8601 timestamp (UTC) indicating when the user first activated the device. Defaults to `null` if not set. |
| `delete_flag` | boolean | Optional  | Flag indicating whether the account is marked for potential deletion. Defaults to `false`. |

#### Example Configuration

Before user activation:

```json
{
  "activation_date": null,
  "delete_flag": false
}
```

After user activation:

```json
{
  "activation_date": "2025-10-10T00:00:00Z",
  "delete_flag": false
}
```

Marked for deletion:

```json
{
  "activation_date": "2025-10-10T00:00:00Z",
  "delete_flag": true
}
```

### DoCommand

The sensor supports the following commands via the `do_command` method:

#### Example DoCommand

```json
{
  "command": "get_activation_state"
}
```

Response:

```json
{
  "activation_date": "2025-10-10T00:00:00Z",
  "delete_flag": false
}
```
